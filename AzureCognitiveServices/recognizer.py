import uuid
from typing import Dict, Optional
from pathlib import Path

from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import FormRecognizerClient

from AzureCognitiveServices.helpers.azure_connection import AzureCredentials


class RecognizeReceiptsFromURLSample(object):
    """Azure recognize class."""

    def recognize_receipts_from_url(self, image_path: Path):  # noqa: C901
        """Azure recognize method."""
        cred_path = Path("config/secrets/credentials.yaml")
        azCredentials = AzureCredentials.load(cred_path)

        endpoint = azCredentials.endpoint
        key = azCredentials.key

        form_recognizer_client = FormRecognizerClient(
            endpoint=endpoint, credential=AzureKeyCredential(key)
        )

        print(image_path)

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
            print("--------Recognizing receipt #{}--------".format(idx + 1))

            add_value_to_dict("ReceiptType", receipt, receipt_data)
            add_value_to_dict("MerchantName", receipt, receipt_data)
            add_value_to_dict("TransactionDate", receipt, receipt_data)

            """ receipt_type = receipt.fields.get("ReceiptType")
            if receipt_type:
                print(
                    "Receipt Type: {} has confidence: {}".format(
                       receipt_type.value, receipt_type.confidence
                    )
                )
                receipt_data["ReceiptType"] = receipt_type.value
                receipt_data["ReceiptConfidence"] = receipt_type.confidence

            merchant_name = receipt.fields.get("MerchantName")
            if merchant_name:
                print(
                    "Merchant Name: {} has confidence: {}".format(
                        merchant_name.value, merchant_name.confidence
                    )
                )
                receipt_data["MerchantName"] = merchant_name.value
                receipt_data["MerchantNameConfidence"] = merchant_name.confidence

            transaction_date = receipt.fields.get("TransactionDate")
            if transaction_date:
                print(
                    "Transaction Date: {} has confidence: {}".format(
                        transaction_date.value, transaction_date.confidence
                    )
                )
                receipt_data["TransactionDate"] = transaction_date.value
                receipt_data["TransactionDateConfidence"] = transaction_date.confidence """

            items = receipt.fields.get("Items")

            items_array = []
            if items:
                print("Receipt items:")
                for idx, item in enumerate(items.value):
                    print("...Item #{}".format(idx + 1))
                    item_name = item.value.get("Name")
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

                    # add_value_to_dict("Name", receipt, items_data)

                    if item_name:
                        items_data["Name"] = item_name.value
                        print(
                            "......Item Name: {} has confidence: {}".format(
                                item_name.value, item_name.confidence
                            )
                        )
                    item_quantity = item.value.get("Quantity")
                    if item_quantity:
                        items_data["Quantity"] = item_quantity.value
                        print(
                            "......Item Quantity: {} has confidence: {}".format(
                                item_quantity.value, item_quantity.confidence
                            )
                        )
                    item_price = item.value.get("Price")
                    if item_price:
                        items_data["Price"] = item_price.value
                        print(
                            "......Individual Item Price: {} has confidence: {}".format(
                                item_price.value, item_price.confidence
                            )
                        )
                    item_total_price = item.value.get("TotalPrice")
                    if item_total_price:
                        items_data["TotalPrice"] = item_total_price.value
                        print(
                            "......Total Item Price: {} has confidence: {}".format(
                                item_total_price.value, item_total_price.confidence
                            )
                        )

            subtotal = receipt.fields.get("Subtotal")
            if subtotal:
                print(
                    "Subtotal: {} has confidence: {}".format(
                        subtotal.value, subtotal.confidence
                    )
                )
                receipt_data["Subtotal"] = subtotal.value
                receipt_data["SubtotalConfidence"] = subtotal.confidence

            tax = receipt.fields.get("Tax")
            if tax:
                print("Tax: {} has confidence: {}".format(tax.value, tax.confidence))
                receipt_data["Tax"] = tax.value
                receipt_data["TaxConfidence"] = tax.confidence

            tip = receipt.fields.get("Tip")
            if tip:
                print("Tip: {} has confidence: {}".format(tip.value, tip.confidence))
                receipt_data["Tip"] = tip.value
                receipt_data["TipConfidence"] = tip.confidence

            total = receipt.fields.get("Total")
            if total:
                print(
                    "Total: {} has confidence: {}".format(total.value, total.confidence)
                )
                receipt_data["Total"] = total.value
                receipt_data["TotalConfidence"] = total.confidence
            print("--------------------------------------")

        form_recognizer_client.close()
        return receipt_data, items_array


def add_value_to_dict(fieldName: str, receipt, data: Dict[str, Optional[str]]):
    """Adds item value and confidence to dict."""
    item = receipt.fields.get(fieldName)

    if item:
        data[fieldName] = item.value
        data[fieldName + "Confidence"] = item.confidence
