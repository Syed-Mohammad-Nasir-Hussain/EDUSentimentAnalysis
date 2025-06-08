from urllib.parse import quote
from sqlalchemy import create_engine
import pandas as pd

def create_mysql_engine(user, password, host, port, database):
    """
    Create a SQLAlchemy engine for a MySQL database.
    
    Args:
        user (str): Username for MySQL.
        password (str): Password for MySQL.
        host (str): Hostname or IP address.
        port (int or str): Port number.
        database (str): Database name.
        
    Returns:
        SQLAlchemy engine object.
    """
    password_encoded = quote(password)  # URL encode the password for special characters
    connection_string = f"mysql+pymysql://{user}:{password_encoded}@{host}:{port}/{database}"
    engine = create_engine(connection_string)
    return engine

def load_feedback_data(engine, query="SELECT * FROM feedback_enriched;"):
    """
    Load data from MySQL using a SQL query into a pandas DataFrame.
    
    Args:
        engine: SQLAlchemy engine object.
        query (str): SQL query string.
        
    Returns:
        pandas.DataFrame containing the query results.
    """
    try:
        df = pd.read_sql(query, con=engine)
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None
