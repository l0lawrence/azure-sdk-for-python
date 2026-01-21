from azure.mgmt.crud.models import BlobContainer, BlobContainerResourceId
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

    # Create resource ID for listing containers in a storage account
    # Note: container_name is not specified for list operations
    resource_id = BlobContainerResourceId(
        resource_group_name=RESOURCE_GROUP,
        storage_account_name=STORAGE_ACCOUNT_NAME,
    )

    response = client.list(
        resource_id=resource_id,
        resource_type=BlobContainer(),
        maxpagesize="2",
    )

    for i in response:
        print(f"Blob container item: {i}")
        print(f"Blob container item properties: {i.properties}")

if __name__ == "__main__":
    main()