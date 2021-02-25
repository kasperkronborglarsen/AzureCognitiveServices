import os
import glob
from pathlib import Path

import click
import pandas as pd

from AzureCognitiveServices.recognizer import RecognizeReceiptsFromURLSample
from AzureCognitiveServices.helpers.csv_helper import save_csv
from AzureCognitiveServices.helpers.logging_helpers import get_logger

logger = get_logger(__name__)


def run_pipeline(image_folder: Path):
    """Runs the full pipeline."""
    logger.debug("Running pipeline")

    sample = RecognizeReceiptsFromURLSample()

    df_receipts = pd.DataFrame(
        columns=[
            "ReceiptId",
            "ReceiptType",
            "ReceiptTypeConfidence",
            "MerchantName",
            "MerchantNameConfidence",
            "TransactionDate",
            "TransactionDateConfidence",
            "Subtotal",
            "SubtotalConfidence",
            "Tax",
            "TaxConfidence",
            "Tip",
            "TipConfidence",
            "Total",
            "TotalConfidence",
        ]
    )
    df_items = pd.DataFrame(
        columns=[
            "ReceiptId",
            "Name",
            "NameConfidence",
            "Quantity",
            "QuantityConfidence",
            "Price",
            "PriceConfidence",
            "TotalPrice",
            "TotalPriceConfidence",
        ]
    )

    for filename in glob.glob(os.path.join(image_folder, "*.*")):

        receipts, items = sample.recognize_receipts_from_url(Path(filename))
        df_receipts = pd.concat([df_receipts, pd.DataFrame([receipts])])
        df_items = pd.concat([df_items, pd.DataFrame(items)])

    save_csv(df_receipts, "data/receiptdata.csv")
    save_csv(df_items, "data/itemsdata.csv")


@click.command(help="Runs the recognizer pipeline.")
@click.option(
    "-i", "--image-folder", type=click.STRING, required=True,
)
def main(image_folder: str):
    """Runs the pipeline."""
    run_pipeline(image_folder=Path(image_folder))


if __name__ == "__main__":
    main()
