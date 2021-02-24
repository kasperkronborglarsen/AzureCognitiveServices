from AzureCognitiveServices.helpers.azure_connection import AzureCredentials
from AzureCognitiveServices.helpers.csv_helper import save_csv
from AzureCognitiveServices.recognizer import RecognizeReceiptsFromURLSample

from pathlib import Path

import click

def run_pipeline(url: str):
    """Runs the full pipeline."""
    sample = RecognizeReceiptsFromURLSample()

    # For testing purpose only
    url = "https://raw.githubusercontent.com/Azure/azure-sdk-for-python/master/sdk/formrecognizer/azure-ai-formrecognizer/tests/sample_forms/receipt/contoso-receipt.png"
    
    df_receipts, df_items = sample.recognize_receipts_from_url(url)

    save_csv(df_receipts, "data/receiptdata.csv")
    save_csv(df_items, "data/itemsdata.csv")


@click.command(help="Runs the recognizer pipeline.")
@click.option(
    "-u",
    "--url",
    type=click.STRING,
    required=True,
)
def main(url: str):
    """Runs the pipeline."""
    run_pipeline(url=url)


if __name__ == "__main__":
    main()