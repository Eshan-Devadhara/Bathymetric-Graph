import os
import pandas as pd


def ensure_directory(path):
    """
    Creates directory if it does not exist.
    """
    if not os.path.exists(path):
        os.makedirs(path)


def read_csv(file_path):
    """
    Read CSV file into pandas DataFrame.
    """
    return pd.read_csv(file_path)


def save_csv(df, file_path):
    """
    Save pandas DataFrame to CSV.
    """
    df.to_csv(file_path, index=False)