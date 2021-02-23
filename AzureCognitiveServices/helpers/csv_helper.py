from pathlib import Path, PurePath

import pandas as pd


def save_csv(df: pd.DataFrame, filepath: Path):
    """Saves dataframe to csv."""
    df.to_csv(PurePath(filepath), index=False)
