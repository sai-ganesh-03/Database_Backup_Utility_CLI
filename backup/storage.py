import boto3
import json
from google.cloud import storage as gcs
from azure.storage.blob import BlobServiceClient
import os
def upload_to_cloud(provider, local_file, bucket_name, config, logger):
    try:
        if provider == 's3':
            # Extract AWS credentials from the config
            aws_access_key = config['aws']['access_key']
            aws_secret_key = config['aws']['secret_key']
            aws_region = config['aws']['region']

            # Create a session with AWS credentials
            session = boto3.Session(
                aws_access_key_id=aws_access_key,
                aws_secret_access_key=aws_secret_key,
                region_name=aws_region
            )
            s3 = session.client('s3')
            s3.upload_file(local_file, bucket_name, local_file.split('/')[-1])
            logger.info(f"Backup uploaded to S3 bucket {bucket_name}")

        elif provider == 'gcs':
            # Load Google Cloud service account key from the config
            service_account_key = config['gcs']['service_account_key']
            # Set the environment variable for Google Cloud authentication
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account_key
            
            client = gcs.Client()
            bucket = client.get_bucket(bucket_name)
            blob = bucket.blob(local_file.split('/')[-1])
            blob.upload_from_filename(local_file)
            logger.info(f"Backup uploaded to Google Cloud bucket {bucket_name}")

        elif provider == 'azure':
            # Extract Azure connection string from the config
            connection_string = config['azure']['connection_string']
            blob_service_client = BlobServiceClient.from_connection_string(connection_string)
            blob_client = blob_service_client.get_blob_client(container=bucket_name, blob=local_file.split('/')[-1])
            with open(local_file, "rb") as data:
                blob_client.upload_blob(data)
            logger.info(f"Backup uploaded to Azure Blob Storage {bucket_name}")

    except Exception as e:
        print(f"An error occurred while uploading to cloud provider {provider}: {e}")
        logger.error(f"An error occurred while uploading to cloud provider {provider}: {e}")
