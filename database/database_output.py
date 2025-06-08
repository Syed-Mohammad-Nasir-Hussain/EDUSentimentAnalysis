import pandas as pd
import json

def save_df_to_db(df: pd.DataFrame, engine, table_name: str, if_exists: str = 'replace'):
    """
    Save a pandas DataFrame to a SQL database table.
    Automatically serializes dict/list columns as JSON strings to avoid insertion errors.
    """
    dict_cols = [col for col in df.columns if df[col].apply(lambda x: isinstance(x, (dict, list))).any()]
    for col in dict_cols:
        df[col] = df[col].apply(json.dumps)

    df.to_sql(name=table_name, con=engine, if_exists=if_exists, index=False)
    print(f"✅ DataFrame saved to table '{table_name}' in database.")
