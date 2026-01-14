from azure.mgmt.crud.models import BlobContainer, BlobContainerPathParams, BlobContainerProperties, LegalHoldProperties
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


    updated_blob = client.update(
        resource_type=BlobContainer(
            properties=BlobContainerProperties(enable_nfs_v3_root_squash=True),
        ),
        url_params=BlobContainerPathParams(
            resource_group_name=RESOURCE_GROUP,
            storage_account_name=STORAGE_ACCOUNT_NAME,
            container_name=CONTAINER_NAME,
        )
    )

    print(f"Updated blob container: {updated_blob}")
    print(f"Updated blob container properties: {updated_blob.properties}")

    # from azure.mgmt.storage import StorageManagementClient
    # from azure.mgmt.storage.models import BlobContainer as BC
    # storage_client = StorageManagementClient(
    #     credential=DefaultAzureCredential(),
    #     subscription_id=SUBSCRIPTION_ID
    # )
    # updated_blob = storage_client.blob_containers.update(
    #     resource_group_name=RESOURCE_GROUP,account_name=STORAGE_ACCOUNT_NAME,container_name=CONTAINER_NAME,
    #     blob_container=BC(enable_nfs_v3_root_squash=True)
    # )
    # print(updated_blob)


main()