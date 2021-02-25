from pathlib import Path, PurePath

import pandas as pd

from AzureCognitiveServices.helpers.logging_helpers import get_logger

logger = get_logger(__name__)


def save_csv(df: pd.DataFrame, filepath: Path):
    """Saves dataframe to csv."""
    logger.debug(f"Saving {df} to {filepath}")
    df.to_csv(PurePath(filepath), index=False)
