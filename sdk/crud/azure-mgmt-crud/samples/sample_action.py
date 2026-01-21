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

    # Create resource ID to identify which container to perform action on
    resource_id = BlobContainerResourceId(
        resource_group_name=RESOURCE_GROUP,
        storage_account_name=STORAGE_ACCOUNT_NAME,
        container_name=CONTAINER_NAME
    )

    print("\n--- Acquiring Lease ---")
    lease_body = BlobContainer.lease_body(
        action="Acquire",
        lease_duration=60  # 60 seconds
    )

    lease_response = client.action(
        resource_id=resource_id,
        action_name=BlobContainer.ACTIONS.LEASE,
        body=lease_body
    )
    print(f"Lease response: {lease_response}")
    lease_id = lease_response.get("leaseId") if lease_response else None
    print(f"Acquired lease ID: {lease_id}")


if __name__ == "__main__":
    main()