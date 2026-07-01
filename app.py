import streamlit as st
import pandas as pd

st.set_page_config(page_title="Redrob Ranker Top 100", page_icon="", layout="wide")

st.title(" Redrob Top 100 Candidates")
st.markdown("This dashboard displays the final Top 100 candidates for the Senior AI Engineer role.")

@st.cache_data
def load_data():
  try:
    df = pd.read_csv("submission.csv")
    return df
  except FileNotFoundError:
    return pd.DataFrame()

df = load_data()

if df.empty:
  st.error("Could not find `submission.csv`. Please run the ranking pipeline first.")
else:
  # Sidebar filters
  st.sidebar.header("🔍 Filter Candidates")
  search_query = st.sidebar.text_input("Search by Candidate ID or Reason keyword:")
  
  # Filtering logic
  filtered_df = df.copy()
  if search_query:
    search_query = search_query.lower()
    filtered_df = filtered_df[
      filtered_df['candidate_id'].str.lower().str.contains(search_query) |
      filtered_df['reason'].str.lower().str.contains(search_query)
    ]
  
  st.success(f"Showing {len(filtered_df)} candidates.")
  
  # Display the dataframe with nice column configs
  st.dataframe(
    filtered_df,
    column_config={
      "rank": st.column_config.NumberColumn("Rank", format="%d 🏅"),
      "candidate_id": "Candidate ID",
      "final_score": st.column_config.NumberColumn("Final Score", format="%.2f / 100"),
      "reason": "AI Reasoning"
    },
    hide_index=True,
    use_container_width=True,
    height=600
  )
  
  st.markdown("---")
  st.markdown("Built by the winning team for the Redrob AI Hackathon.")
