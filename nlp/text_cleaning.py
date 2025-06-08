import re
import unicodedata
from bs4 import BeautifulSoup

def fill_nulls(df, col='feedback_text'):
    """
    Fill null (NaN) values in a specified DataFrame column with empty strings.
    
    Args:
        df (pandas.DataFrame): Input DataFrame.
        col (str): Column name to fill nulls in. Default is 'feedback_text'.
        
    Returns:
        pandas.DataFrame: DataFrame with nulls filled in the specified column.
    """
    df[col] = df[col].fillna("")
    return df

def remove_html(text):
    """
    Remove HTML tags from a given text string.
    
    Args:
        text (str): Input text containing HTML.
        
    Returns:
        str: Text with HTML tags removed.
    """
    return BeautifulSoup(text, "html.parser").get_text()

def remove_special_characters(text):
    """
    Remove special characters from text by normalizing unicode characters to ASCII.
    This removes accents and non-ASCII characters.
    
    Args:
        text (str): Input text.
        
    Returns:
        str: ASCII-normalized text with special characters removed.
    """
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8", "ignore")
    return text

def lowercase(text):
    """
    Convert all characters in the text to lowercase.
    
    Args:
        text (str): Input text.
        
    Returns:
        str: Lowercase version of the input text.
    """
    return text.lower()

def remove_punctuation(text):
    """
    Remove all punctuation characters from the text, replacing them with spaces.
    
    Args:
        text (str): Input text.
        
    Returns:
        str: Text without punctuation.
    """
    return re.sub(r'[^\w\s]', ' ', text)

def remove_numbers(text):
    """
    Remove all digit characters from the text, replacing them with spaces.
    
    Args:
        text (str): Input text.
        
    Returns:
        str: Text with numbers removed.
    """
    return re.sub(r'\d+', ' ', text)
