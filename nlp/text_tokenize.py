import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download required nltk data (only once)
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

lemmatizer = WordNetLemmatizer()
# Base stopwords
base_stop_words = set(stopwords.words('english'))

# Customize stopwords
custom_stop_words = base_stop_words - {'not', 'no'}
custom_stop_words.update({'uhh'})  # separate and combined for safety

def tokenize(text):
    """
    Tokenize input text into a list of words.
    
    Args:
        text (str): Input text string.
    
    Returns:
        list: List of word tokens.
    """
    return nltk.word_tokenize(text)

def remove_stopwords_func(tokens):
    """
    Remove English stopwords from a list of tokens.
    
    Args:
        tokens (list): List of word tokens.
    
    Returns:
        list: Tokens with stopwords removed.
    """
    return [word for word in tokens if word.lower() not in custom_stop_words]

def lemmatize_tokens(tokens):
    """
    Lemmatize a list of word tokens.
    
    Args:
        tokens (list): List of word tokens.
    
    Returns:
        list: List of lemmatized tokens.
    """
    return [lemmatizer.lemmatize(word) for word in tokens]
