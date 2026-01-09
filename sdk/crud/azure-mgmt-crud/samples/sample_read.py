from azure.mgmt.crud.models import CustomLocation
from azure.mgmt.crud import CrudClient

from azure.identity import DefaultAzureCredential
import os
SUBSCRIPTION_ID = os.environ["SUBSCRIPTION_ID"]
RESOURCE_GROUP = os.environ["RESOURCE_GROUP"] 
RESOURCE_NAME = os.environ["RESOURCE_NAME"]

def main():
    client = CrudClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    response = client.read(
        resource_group_name=RESOURCE_GROUP,
        resource_name=RESOURCE_NAME,
        resource_type=CustomLocation,
    )
    print(response)

if __name__ == "__main__":
    main()