import pandas as pd
from database.database_input import create_mysql_engine, load_feedback_data
from database.database_output import save_df_to_db
from nlp.preprocess import preprocess_feedback
from analysis.sentiment import analyze_sentiment
from nlp.keyword_extraction import extract_keywords, get_keyword_frequencies_by_sentiment_and_department
from analysis.accuracy import evaluate_sentiment_predictions
from dotenv import load_dotenv
import os

load_dotenv()  # load from .env file

def main():
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = int(os.getenv("DB_PORT"))
    database = os.getenv("DB_NAME")

    engine = create_mysql_engine(user, password, host, port, database)
    df = load_feedback_data(engine)
    df = preprocess_feedback(df, text_col='feedback_text')

    # Sentiment label directly
    df['sentiment_label'] = df['clean_feedback'].apply(analyze_sentiment)

    # Extract keywords
    df['keywords'] = df['clean_feedback'].apply(extract_keywords)

    return df, engine


if __name__ == "__main__":
    df, engine = main()
    print(df.head())
    print(df['sentiment_label'].value_counts())

    # Save feedback + sentiment + keywords to DB (append mode)
    save_df_to_db(df, engine, table_name='sentiment_analysis', if_exists='append')

    # Save keyword frequencies per sentiment per department to DB (append mode)
    keyword_df = get_keyword_frequencies_by_sentiment_and_department(df)
    save_df_to_db(keyword_df, engine, table_name='keywords_sentiment_summary', if_exists='append')

    # Save predictions to CSV for evaluation
    df.to_csv('data/predictions.csv', index=False)

    # Run evaluation only (no saving)
    evaluate_sentiment_predictions('data/student_labelled_data.csv', 'data/predictions.csv')
