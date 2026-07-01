# Project Notes: Redrob Hackathon

## The Goal
We need to rank 100k candidates for an AI engineer role. The constraints are pretty tight: CPU only, under 5 minutes, no internet. So no live LLM API calls during the ranking. We have to do this entirely with fast, local math.

## Iteration 1: The Basics
Started by looking at the `sample_candidates.json`. The data is pretty nested. Wrote `01_data_exploration.ipynb` to flatten it out.
Drafted a basic scoring formula in `02_scoring_formula.ipynb`. Gave arbitrary points for core skills like PyTorch vs nice-to-have skills like Docker. 
Issue: Arbitrary weights are subjective and feel wrong. 

## Iteration 2: Dealing with Scaling
Looked into feature scaling in `02b_scaling_exploration.ipynb`. We initially thought about using Min-Max scaling or standard Z-scores. 
Realized a massive problem: Min-Max learns the "max" from the training set. If the 100k dataset has a guy with 10x more GitHub activity than our sample, his score breaks 1.0 and throws off the whole distribution. We need something memoryless.
Decision: Stick to pure mathematical transforms (Log, Sqrt, CubeRoot).
To figure out which one to use per feature, we implemented a Shapiro-Wilk test to just pick whichever transform makes the data look most normal.

## Iteration 3: Fixing Outliers
We added a Z-score filter to drop "honeypots" and inactive candidates.
It didn't work well on the skewed data. `days_inactive` is heavily right-skewed (most people are active, a few have been gone for 800 days). The massive outliers were pulling the standard deviation up so high that the Z > 3 threshold wasn't catching the medium-bad outliers.
Pivoted to using IQR (Interquartile Range) instead. Since it uses percentiles (Q1, Q3), the extreme 800-day guys don't shift the threshold. Dropped anyone above Q3 + 1.5*IQR. Worked perfectly.

## Iteration 4: Dynamic Weights
Since arbitrary weights were bugging us, we looked into entropy weighting.
By calculating the Shannon Entropy of each feature's percentile distribution, we can let the data decide the weights. If everyone has a high "interview completion rate", that feature has low entropy (low variance) and gets a lower weight. If GitHub scores are wildly different across candidates, it gets a higher weight. 

## Final Architecture
Everything is merged into `03_final_pipeline.ipynb`.
1. Load JSONL
2. Extract features
3. Shapiro-Wilk auto-transforms
4. IQR honeypot dropping
5. Percentile rank remaining pool
6. Entropy weighting
7. Final score (0-100)

Pipeline takes about 10 seconds. Output looks solid. Built a quick Streamlit app (`app.py`) to show off the results for the judges.
