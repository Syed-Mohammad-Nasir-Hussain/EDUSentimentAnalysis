import streamlit as st
import pandas as pd
import sqlalchemy
import matplotlib.pyplot as plt
import seaborn as sns
import urllib.parse
from dotenv import load_dotenv
import os

load_dotenv()  # load from .env file

# Use the same DB connection parameters or move them to a config file if you prefer
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
PORT = int(os.getenv("DB_PORT"))
DATABASE = os.getenv("DB_NAME")
PASSWORD = urllib.parse.quote(PASSWORD)
SQL_CONNECTION_STRING = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

@st.cache_data(ttl=300)
def load_sentiment_analysis():
    engine = sqlalchemy.create_engine(SQL_CONNECTION_STRING)
    query = "SELECT * FROM sentiment_analysis"
    return pd.read_sql(query, engine)

@st.cache_data(ttl=300)
def load_keywords_summary():
    engine = sqlalchemy.create_engine(SQL_CONNECTION_STRING)
    query = "SELECT * FROM keywords_sentiment_summary"
    return pd.read_sql(query, engine)

def main():
    st.title("EDU Sentiment Analysis Dashboard")

    sentiment_df = load_sentiment_analysis()
    keywords_df = load_keywords_summary()

    departments = sentiment_df['department_name'].unique()
    selected_dept = st.sidebar.selectbox("Select Department", options=['All'] + list(departments))

    sentiment_df['date'] = pd.to_datetime(sentiment_df['date'])
    min_date, max_date = sentiment_df['date'].min(), sentiment_df['date'].max()
    date_range = st.sidebar.date_input("Select Date Range", value=(min_date, max_date), min_value=min_date, max_value=max_date)

    # Filter by department
    if selected_dept != 'All':
        sentiment_df = sentiment_df[sentiment_df['department_name'] == selected_dept]

    # Filter by date range
    start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    sentiment_df = sentiment_df[(sentiment_df['date'] >= start_date) & (sentiment_df['date'] <= end_date)]

    st.subheader(f"Summary Metrics for Department: {selected_dept}")
    total_feedback = len(sentiment_df)
    pos_count = (sentiment_df['sentiment_label'] == 'positive').sum()
    neu_count = (sentiment_df['sentiment_label'] == 'neutral').sum()
    neg_count = (sentiment_df['sentiment_label'] == 'negative').sum()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Feedback", total_feedback)
    col2.metric("Positive", pos_count)
    col3.metric("Neutral", neu_count)
    col4.metric("Negative", neg_count)

    st.subheader("Sentiment Distribution")
    sentiment_counts = sentiment_df['sentiment_label'].value_counts()
    fig, ax = plt.subplots()
    sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, palette='pastel', ax=ax)
    ax.set_ylabel("Count")
    ax.set_xlabel("Sentiment")
    st.pyplot(fig)

    st.subheader("Sentiment Over Time")
    sentiment_time = sentiment_df.groupby(['date', 'sentiment_label']).size().unstack(fill_value=0)
    st.line_chart(sentiment_time)

    st.subheader("Top Keywords by Sentiment")
    if selected_dept != 'All':
        keywords_filtered = keywords_df[keywords_df['department'] == selected_dept]
    else:
        keywords_filtered = keywords_df.copy()

    keyword_sentiment = st.selectbox("Select Sentiment", ['positive', 'neutral', 'negative'])
    keywords_filtered = keywords_filtered[keywords_filtered['sentiment_label'] == keyword_sentiment]

    top_keywords = keywords_filtered.sort_values('count', ascending=False).head(15)
    st.table(top_keywords[['keyword', 'count']])

    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.barplot(data=top_keywords, x='count', y='keyword', hue='sentiment_label', dodge=False, ax=ax2)
    ax2.set_title(f"Top Keywords - {keyword_sentiment.title()}")
    st.pyplot(fig2)

    # ✅ New Section: Detailed Feedback Table
    st.subheader("Detailed Feedback Table")

    sentiment_filter = st.multiselect(
        "Filter by Sentiment Label",
        options=sentiment_df['sentiment_label'].unique(),
        default=sentiment_df['sentiment_label'].unique()
    )

    filtered_table = sentiment_df[sentiment_df['sentiment_label'].isin(sentiment_filter)]

    st.dataframe(
        filtered_table[['date', 'department_name', 'sentiment_label', 'feedback_text']],
        use_container_width=True,
        height=400
    )

if __name__ == "__main__":
    main()
