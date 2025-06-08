from nlp.text_cleaning import (
    fill_nulls,
    remove_html,
    remove_special_characters,
    lowercase,
    remove_punctuation,
    remove_numbers,
)

from nlp.text_tokenize import tokenize, remove_stopwords_func, lemmatize_tokens


def clean_text_pipeline(text):
    """
    Apply a sequence of text cleaning and preprocessing steps to a text string.
    
    Steps include:
    - Remove HTML tags
    - Remove special/unicode characters
    - Convert to lowercase
    - Remove punctuation
    - Remove numbers
    - Tokenize text
    - Remove stopwords
    - Lemmatize tokens
    
    Args:
        text (str): Raw input text string.
    
    Returns:
        str: Cleaned and preprocessed text as a single space-joined string of tokens.
    """
    text = remove_html(text)
    text = remove_special_characters(text)
    text = lowercase(text)
    text = remove_punctuation(text)
    text = remove_numbers(text)
    tokens = tokenize(text)
    tokens = remove_stopwords_func(tokens)
    tokens = lemmatize_tokens(tokens)
    return " ".join(tokens)

def preprocess_feedback(df, text_col='feedback_text'):
    """
    Preprocess a pandas DataFrame by filling nulls and creating a cleaned text column.
    
    Args:
        df (pandas.DataFrame): Input DataFrame containing feedback text.
        text_col (str): Name of the column containing raw text to preprocess. Default is 'feedback_text'.
    
    Returns:
        pandas.DataFrame: DataFrame with a new column 'clean_feedback' containing cleaned text.
    """
    df = fill_nulls(df, text_col)
    df['clean_feedback'] = df[text_col].apply(clean_text_pipeline)
    return df
