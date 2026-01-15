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

    # Example 1: Discover available actions
    print(f"Available actions: {BlobContainer.get_available_actions()}")
    print(f"Actions enum: {[action.value for action in BlobContainer.ACTIONS]}")

    # Example 2: Set legal hold on container
    print("\n--- Setting Legal Hold ---")
    legal_hold_body = BlobContainer.set_legal_hold_body(tags=["legal-tag-1", "compliance-tag"])
    
    response = client.action(
        resource_type=BlobContainer(),
        action_name=BlobContainer.ACTIONS.SET_LEGAL_HOLD,  # or just "setLegalHold"
        url_params=BlobContainerPathParams(
            resource_group_name=RESOURCE_GROUP,
            storage_account_name=STORAGE_ACCOUNT_NAME,
            container_name=CONTAINER_NAME
        ),
        body=legal_hold_body
    )
    print(f"Set legal hold response: {response}")

    # Example 3: Acquire a lease on the container
    print("\n--- Acquiring Lease ---")
    lease_body = BlobContainer.lease_body(
        action="Acquire",
        lease_duration=60  # 60 seconds
    )
    
    lease_response = client.action(
        resource_type=BlobContainer(),
        action_name=BlobContainer.ACTIONS.LEASE,
        url_params=BlobContainerPathParams(
            resource_group_name=RESOURCE_GROUP,
            storage_account_name=STORAGE_ACCOUNT_NAME,
            container_name=CONTAINER_NAME
        ),
        body=lease_body
    )
    print(f"Lease response: {lease_response}")
    lease_id = lease_response.get("leaseId") if lease_response else None
    print(f"Acquired lease ID: {lease_id}")

    # Example 4: Release the lease
    if lease_id:
        print("\n--- Releasing Lease ---")
        release_body = BlobContainer.lease_body(
            action="Release",
            lease_id=lease_id
        )
        
        release_response = client.action(
            resource_type=BlobContainer(),
            action_name=BlobContainer.ACTIONS.LEASE,
            url_params=BlobContainerPathParams(
                resource_group_name=RESOURCE_GROUP,
                storage_account_name=STORAGE_ACCOUNT_NAME,
                container_name=CONTAINER_NAME
            ),
            body=release_body
        )
        print(f"Release response: {release_response}")

    # Example 5: Clear legal hold
    print("\n--- Clearing Legal Hold ---")
    clear_hold_body = BlobContainer.clear_legal_hold_body(tags=["legal-tag-1", "compliance-tag"])
    
    clear_response = client.action(
        resource_type=BlobContainer(),
        action_name=BlobContainer.ACTIONS.CLEAR_LEGAL_HOLD,
        url_params=BlobContainerPathParams(
            resource_group_name=RESOURCE_GROUP,
            storage_account_name=STORAGE_ACCOUNT_NAME,
            container_name=CONTAINER_NAME
        ),
        body=clear_hold_body
    )
    print(f"Clear legal hold response: {clear_response}")
    
    print("\n--- Action Examples Complete ---")


if __name__ == "__main__":
    main()