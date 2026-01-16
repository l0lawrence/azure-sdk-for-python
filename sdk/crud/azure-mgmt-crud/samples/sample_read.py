from azure.mgmt.crud.models import BlobContainer, BlobContainerPathParams
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

    response = client.read(resource_type=BlobContainer(),url_params=BlobContainerPathParams(
        resource_group_name=RESOURCE_GROUP,
        storage_account_name=STORAGE_ACCOUNT_NAME,
        container_name=CONTAINER_NAME,
    ))

    print(response)


    if response:
        logger.info("Read BlobContainer successfully.\n")
        logger.info(f"BlobContainer details: {response.to_dict()} \n")
        logger.info(f"BlobContainer name: {response.name} \n")
        logger.info(f"BlobContainer properties: {response.properties} \n")
        logger.info(f"Is blobContainer {isinstance(response, BlobContainer)} \n")


if __name__ == "__main__":
    main()