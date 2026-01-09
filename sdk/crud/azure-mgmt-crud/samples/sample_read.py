from azure.mgmt.crud.models import CustomLocation, BlobContainer
from azure.mgmt.crud import CrudClient

from azure.identity import DefaultAzureCredential
import os
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
handler = logging.StreamHandler()
logger.addHandler(handler)

SUBSCRIPTION_ID = os.environ["SUBSCRIPTION_ID"]
RESOURCE_GROUP = os.environ["RESOURCE_GROUP"] 
CONTAINER_NAME = os.environ["CONTAINER_NAME"]
STORAGE_ACCOUNT_NAME = os.environ["STORAGE_ACCOUNT_NAME"]


def main():
    client = CrudClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    logger.debug(f"Initialized CrudClient {client}")

    response = client.read(resource_type=BlobContainer(
        resource_group_name=RESOURCE_GROUP,
        storage_account_name=STORAGE_ACCOUNT_NAME,
        container_name=CONTAINER_NAME
    ))
    print(response)

if __name__ == "__main__":
    main()