# Redrob Ranker - AI Candidate Ranking Engine

This repository contains our submission for the Redrob AI Hackathon. 

## Overview
We built a candidate ranking engine to process 100,000 JSONL candidate profiles and output the top 100 matches for a Senior AI Engineer role. 

Our main focus was building a system that is robust against **distribution shift**. Traditional approaches like Min-Max scaling or Z-score outlier detection often fail on new data if the distributions are skewed or if new max values appear. We solved this using a purely statistical pipeline.

## How it works
1. **Feature Extraction**: We extract technical skills (PyTorch, Transformers, RAG) and behavioral signals (recruiter response rate, GitHub activity).
2. **Auto-Scaling (Shapiro-Wilk)**: Instead of hardcoding transformations, the system runs the Shapiro-Wilk test to dynamically choose the best mathematical transform (Log, Sqrt, CubeRoot) for each feature.
3. **Outlier/Honeypot Removal (IQR)**: Since our red-flag signals (like `days_inactive`) are heavily right-skewed, we use the Interquartile Range (IQR) method (drop if > Q3 + 1.5*IQR) instead of standard deviation to avoid missing extreme outliers.
4. **Ranking & Weighting**: Features are converted to Percentile Ranks [0, 1]. We then use **Shannon Entropy** to dynamically assign weights to each feature (higher variance = higher weight). 
5. **Output**: The system calculates a final score (0-100) and outputs `submission.csv` with the top 100 candidates and their dynamically generated reasoning.

## Files
- `01_data_exploration.ipynb`: Initial data parsing.
- `02b_scaling_exploration.ipynb`: Research on distributions and scalers.
- `03_final_pipeline.ipynb`: The main execution script. Run this to generate the CSV.
- `app.py`: A Streamlit UI to visualize the final results.
- `Project_History.md`: Notes on our engineering decisions and iterations.

## Execution
The entire pipeline runs in under 15 seconds on a standard CPU using vectorized pandas operations.
