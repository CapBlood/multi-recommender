"""
This is a boilerplate pipeline 'drop_nan_column'
generated using Kedro 0.18.4
"""

def drop_nan_column(df, target_column):
    return df.copy()[df[target_column].notna()]
