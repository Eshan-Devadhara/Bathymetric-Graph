import pandas as pd
from utils.file_utils import save_csv


def clean_depth_data(df):
    """
    Remove invalid depth points.
    """

    df = df.dropna()

    df = df[df["depth"] > 0]

    return df


def preprocess_data(df, output_path):
    """
    Full preprocessing pipeline.
    """

    df_clean = clean_depth_data(df)

    save_csv(df_clean, output_path)

    return df_clean