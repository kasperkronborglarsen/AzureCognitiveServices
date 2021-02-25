import uuid
from typing import Dict, Optional
from pathlib import Path

from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import FormRecognizerClient

from AzureCognitiveServices.helpers.logging_helpers import get_logger
from AzureCognitiveServices.helpers.azure_connection import AzureCredentials

logger = get_logger(__name__)


class RecognizeReceiptsFromURLSample(object):
    """Azure recognize class."""

    def recognize_receipts_from_folder(self, image_path: Path):  # noqa: C901
        """Azure recognize method."""
        cred_path = Path("config/secrets/credentials.yaml")
        azCredentials = AzureCredentials.load(cred_path)

        endpoint = azCredentials.endpoint
        key = azCredentials.key

        form_recognizer_client = FormRecognizerClient(
            endpoint=endpoint, credential=AzureKeyCredential(key)
        )

        print(image_path)
        logger.debug(f"Recognizing image: {image_path}")

        with open(Path(image_path), "rb") as f:
            poller = form_recognizer_client.begin_recognize_receipts(
                receipt=f, content_type="image/jpeg"
            )
        receipts = poller.result()

        receipt_id = str(uuid.uuid4())

        receipt_data = {
            "ReceiptId": receipt_id,
            "ReceiptType": None,
            "ReceiptTypeConfidence": None,
            "MerchantName": None,
            "MerchantNameConfidence": None,
            "TransactionDate": None,
            "TransactionDateConfidence": None,
            "Subtotal": None,
            "SubtotalConfidence": None,
            "Tax": None,
            "TaxConfidence": None,
            "Tip": None,
            "TipConfidence": None,
            "Total": None,
            "TotalConfidence": None,
        }

        for idx, receipt in enumerate(receipts):

            add_receipt_field_to_dict("ReceiptType", receipt, receipt_data)
            add_receipt_field_to_dict("MerchantName", receipt, receipt_data)
            add_receipt_field_to_dict("TransactionDate", receipt, receipt_data)

            items = receipt.fields.get("Items")

            items_array = []
            if items:
                print("Receipt items:")
                for idx, item in enumerate(items.value):
                    logger.debug(f"Identified item #{idx + 1}")
                    # item_name = item.value.get("Name")
                    items_data = {
                        "ReceiptId": receipt_id,
                        "Name": None,
                        "NameConfidence": None,
                        "Quantity": None,
                        "QuantityConfidence": None,
                        "Price": None,
                        "PriceConfidence": None,
                        "TotalPrice": None,
                        "TotalPriceConfidence": None,
                    }
                    items_array.append(items_data)

                    add_receipt_item_to_dict("Name", item, items_data)
                    add_receipt_item_to_dict("Quantity", item, items_data)
                    add_receipt_item_to_dict("Price", item, items_data)
                    add_receipt_item_to_dict("TotalPrice", item, items_data)

            add_receipt_field_to_dict("Subtotal", receipt, receipt_data)
            add_receipt_field_to_dict("Tax", receipt, receipt_data)
            add_receipt_field_to_dict("Tip", receipt, receipt_data)
            add_receipt_field_to_dict("Total", receipt, receipt_data)

        form_recognizer_client.close()
        return receipt_data, items_array


def add_receipt_field_to_dict(fieldName: str, receipt, data: Dict[str, Optional[str]]):
    """Adds receipt field value and confidence to dict."""
    logger.debug(f"Adds receipt field {fieldName} to dictionary")
    receipt_field = receipt.fields.get(fieldName)

    if receipt_field:
        data[fieldName] = receipt_field.value
        data[fieldName + "Confidence"] = receipt_field.confidence


def add_receipt_item_to_dict(fieldName: str, item, data: Dict[str, Optional[str]]):
    """Adds item field value and confidence to dict."""
    logger.debug(f"Adds item field {fieldName} to dictionary")
    item_field = item.value.get(fieldName)

    if item_field:
        data[fieldName] = item_field.value
        data[fieldName + "Confidence"] = item_field.confidence
