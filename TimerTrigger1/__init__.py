import logging
import azure.functions as func
import datetime
import os
import csv

import xmlrpc.client
import azure.functions as func
from azure.storage.blob import BlobServiceClient

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    url = "https://url.odoo.com"
    database = "dbname"
    username = "user@messagerie.fr"
    mdp = "password"

    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))

    uid = common.authenticate(database, username, mdp, {})

    if uid:
        logging.info("Authentication Success")
    else:
        logging.error("Authentication Failed")
        return

    # Define the models endpoint
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

    # Fetch all fields and all rows from "pos.order.line" table that is in Odoo
    pos_order_lines = models.execute_kw(database, uid, mdp,
        'pos.order.line', 'search_read',
        [[]],  # No search criteria to get all rows
        {}  # No fields specified to get all fields
    )

    if pos_order_lines:
        # Generate the CSV content with the name of the table I want to load
        csv_file_path = "/tmp/temp_file.csv"
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=pos_order_lines[0].keys())
            writer.writeheader()
            for row in pos_order_lines:
                writer.writerow(row)

        # Upload the CSV file to Azure Blob Storage using infos
        connect_str = 'mettre-la-clé-ici'
        logging.info(connect_str)
        #This the name of the container I created in Azure Storage
        container_name = "odoo-csv-container"
        blob_name = f"pos_order_line_{utc_timestamp}.csv"

        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

        with open(csv_file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)

        logging.info(f"Data exported to {container_name}/{blob_name} successfully")
    else:
        logging.info("No data found in pos.order.line table")