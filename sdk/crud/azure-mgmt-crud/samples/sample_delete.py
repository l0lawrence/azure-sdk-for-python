from azure.mgmt.crud.models import BlobContainerResourceId
from azure.mgmt.crud import CrudClient

from azure.identity import DefaultAzureCredential
import os
import logging

logger = logging.getLogger()
handler = logging.StreamHandler()
logger.addHandler(handler)
logger.setLevel(logging.INFO)

SUBSCRIPTION_ID = os.environ["SUBSCRIPTION_ID"]
RESOURCE_GROUP = os.environ["RESOURCE_GROUP"]
CONTAINER_NAME = os.environ["CONTAINER_NAME"]
STORAGE_ACCOUNT_NAME = os.environ["STORAGE_ACCOUNT_NAME"]


def main():
    client = CrudClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    logger.info(f"Initialized CrudClient {client}")

    # Create resource ID to identify which container to delete
    resource_id = BlobContainerResourceId(
        resource_group_name=RESOURCE_GROUP,
        storage_account_name=STORAGE_ACCOUNT_NAME,
        container_name=CONTAINER_NAME,
    )

    client.delete(resource_id=resource_id)

main()