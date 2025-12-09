#!/usr/bin/env python3
"""
Simple test to verify the factory instantiation works correctly.
"""

import os
from azure.mgmt.all import ManagementClient
from azure.mgmt.all.models import ConfigurationStore
from azure.identity import DefaultAzureCredential

def test_factory_instantiation():
    """Test that the factory instantiation works correctly."""
    
    # Create management client
    client = ManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=os.environ["AZURE_SUBSCRIPTION_ID"],
    )
    
    # Test getting AppConfiguration factory
    print("Testing AppConfiguration factory instantiation...")
    app_config = client("Microsoft.AppConfiguration")
    print(f"✓ Got factory: {type(app_config)}")
    print(f"✓ Service provider: {app_config.service_provider}")
    print(f"✓ Subscription ID: {app_config.subscription_id}")
    print(f"✓ Base URL: {app_config.base_url}")
    

    resource_group = os.environ["AZURE_RESOURCE_GROUP"]

    # create a new configuration store
    print("Creating a new configuration store...")
    config_store = ConfigurationStore(sku={"name": "Standard"}, location="eastus")

    output = app_config.configuration_stores.begin_create(resource_group, "myconfigstore", config_store)
    print(output)
  
    # create a new configuration store
if __name__ == "__main__":
    test_factory_instantiation()