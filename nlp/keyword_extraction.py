import yake
from collections import Counter
import ast
import pandas as pd

# Define unwanted filler keywords to exclude
UNWANTED_KEYWORDS = {"uh", "uhh", "umm", "um", "like", "i mean"}

def extract_keywords(text, top_n=5, max_ngram=2):
    kw_extractor = yake.KeywordExtractor(lan="en", n=max_ngram, top=top_n)
    keywords = kw_extractor.extract_keywords(text)
    # Filter out unwanted keywords
    return [kw for kw, _ in keywords if kw.lower().strip() not in UNWANTED_KEYWORDS]

def get_keyword_frequencies_by_sentiment_and_department(df):
    all_records = []

    for sentiment in ['positive', 'neutral', 'negative']:
        sentiment_df = df[df['sentiment_label'] == sentiment]

        for department in sentiment_df['department_name'].unique():
            dept_df = sentiment_df[sentiment_df['department_name'] == department]

            keywords_flat = []
            for kws in dept_df['keywords']:
                if isinstance(kws, str):
                    kws = ast.literal_eval(kws)
                if isinstance(kws, list):
                    # Filter again if needed
                    keywords_flat.extend([kw for kw in kws if kw.lower().strip() not in UNWANTED_KEYWORDS])

            counter = Counter(keywords_flat)
            for kw, count in counter.items():
                all_records.append({
                    'department': department,
                    'sentiment_label': sentiment,
                    'keyword': kw,
                    'count': count
                })

    keyword_summary_df = pd.DataFrame(all_records)
    print(keyword_summary_df.head())
    return keyword_summary_df
