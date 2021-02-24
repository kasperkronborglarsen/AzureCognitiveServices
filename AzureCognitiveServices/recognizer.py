# coding: utf-8

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
FILE: sample_recognize_receipts_from_url.py
DESCRIPTION:
    This sample demonstrates how to recognize and extract common fields from a receipt URL,
    using a pre-trained receipt model. For a suggested approach to extracting information
    from receipts, see sample_strongly_typed_recognized_form.py.
    See fields found on a receipt here:
    https://aka.ms/formrecognizer/receiptfields
USAGE:
    python sample_recognize_receipts_from_url.py
    Set the environment variables with your own values before running the sample:
    1) AZURE_FORM_RECOGNIZER_ENDPOINT - the endpoint to your Cognitive Services resource.
    2) AZURE_FORM_RECOGNIZER_KEY - your Form Recognizer API key
"""
from AzureCognitiveServices.helpers.azure_connection import AzureCredentials
from AzureCognitiveServices.helpers.csv_helper import save_csv
from pathlib import Path

import pandas as pd



class RecognizeReceiptsFromURLSample(object):

    def recognize_receipts_from_url(self, url: str):
        # [START recognize_receipts_from_url]
        from azure.core.credentials import AzureKeyCredential
        from azure.ai.formrecognizer import FormRecognizerClient

        cred_path = Path("config/secrets/credentials.yaml")
        azCredentials = AzureCredentials.load(cred_path)

        endpoint = azCredentials.endpoint
        key = azCredentials.key

        form_recognizer_client = FormRecognizerClient(
            endpoint=endpoint, credential=AzureKeyCredential(key)
        )
        # https://raw.githubusercontent.com/Azure/azure-sdk-for-python/master/sdk/formrecognizer/azure-ai-formrecognizer/tests/sample_forms/receipt/contoso-receipt.png
        # url = "https://i.ibb.co/2dCWks3/download.jpg"
        
        poller = form_recognizer_client.begin_recognize_receipts_from_url(receipt_url=url)
        receipts = poller.result()

        df_receipt = pd.DataFrame()
        df_items = pd.DataFrame()
        receipt_data = {"ReceiptType": None, "ReceiptConfidence": None, "MerchantName": None, "MerchantNameConfidence": None, "TransactionDate": None, "TransactionDateConfidence": None}
        items_data = {"Name": None, "Quantity": None, "Price": None, "TotalPrice": None}

        for idx, receipt in enumerate(receipts):
            print("--------Recognizing receipt #{}--------".format(idx+1))
            receipt_type = receipt.fields.get("ReceiptType")
            if receipt_type:
                print("Receipt Type: {} has confidence: {}".format(receipt_type.value, receipt_type.confidence))
                receipt_data["ReceiptType"] = receipt_type.value
                receipt_data["ReceiptConfidence"] = receipt_type.confidence

            merchant_name = receipt.fields.get("MerchantName")
            if merchant_name:
                print("Merchant Name: {} has confidence: {}".format(merchant_name.value, merchant_name.confidence))
                receipt_data["MerchantName"] = merchant_name.value
                receipt_data["MerchantNameConfidence"] = merchant_name.confidence
            
            transaction_date = receipt.fields.get("TransactionDate")
            if transaction_date:
                print("Transaction Date: {} has confidence: {}".format(transaction_date.value, transaction_date.confidence))
                receipt_data["TransactionDate"] = transaction_date.value
                receipt_data["TransactionDateConfidence"] = transaction_date.confidence
            
            items = receipt.fields.get("Items").value
            if items:
                print("Receipt items:")
                for idx, item in enumerate(receipt.fields.get("Items").value):
                    print("...Item #{}".format(idx+1))
                    item_name = item.value.get("Name")
                    if item_name:
                        items_data["Name"] = item_name.value
                        print("......Item Name: {} has confidence: {}".format(item_name.value, item_name.confidence))
                    item_quantity = item.value.get("Quantity")
                    if item_quantity:
                        items_data["Quantity"] = item_quantity.value
                        print("......Item Quantity: {} has confidence: {}".format(item_quantity.value, item_quantity.confidence))
                    item_price = item.value.get("Price")
                    if item_price:
                        items_data["Price"] = item_price.value
                        print("......Individual Item Price: {} has confidence: {}".format(item_price.value, item_price.confidence))
                    item_total_price = item.value.get("TotalPrice")
                    if item_total_price:
                        items_data["TotalPrice"] = item_total_price.value
                        print("......Total Item Price: {} has confidence: {}".format(item_total_price.value, item_total_price.confidence))
            
            subtotal = receipt.fields.get("Subtotal")
            if subtotal:
                print("Subtotal: {} has confidence: {}".format(subtotal.value, subtotal.confidence))
            
            tax = receipt.fields.get("Tax")
            if tax:
                print("Tax: {} has confidence: {}".format(tax.value, tax.confidence))
            
            tip = receipt.fields.get("Tip")
            if tip:
                print("Tip: {} has confidence: {}".format(tip.value, tip.confidence))
            
            total = receipt.fields.get("Total")
            if total:
                print("Total: {} has confidence: {}".format(total.value, total.confidence))
            print("--------------------------------------")
        # [END recognize_receipts_from_url]

        df_receipt = pd.DataFrame([receipt_data])
        df_items = pd.DataFrame([items_data])
        return df_receipt, df_items


if __name__ == '__main__':
    sample = RecognizeReceiptsFromURLSample()
    df_receipts, df_items = sample.recognize_receipts_from_url(Path("config/secrets/credentials.yaml"))

    save_csv(df, "data/output.csv")
