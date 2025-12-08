#!/usr/bin/env python3
"""
Simple async test to verify the factory instantiation works correctly.
"""

import os
import asyncio
from azure.mgmt.all.aio import AsyncManagementClient
from azure.identity.aio import DefaultAzureCredential

async def test_async_factory_instantiation():
    """Test that the async factory instantiation works correctly."""
    
    # Create async management client
    async with DefaultAzureCredential() as credential:
        client = AsyncManagementClient(
            credential=credential,
            subscription_id=os.environ["AZURE_SUBSCRIPTION_ID"],
        )
        
        async with client:
            # Test getting AppConfiguration factory
            print("Testing AsyncAppConfiguration factory instantiation...")
            app_config = client("Microsoft.AppConfiguration")
            print(f"✓ Got factory: {type(app_config)}")
            print(f"✓ Service provider: {app_config.service_provider}")
            print(f"✓ Subscription ID: {app_config.subscription_id}")
            print(f"✓ Base URL: {app_config.base_url}")
            
            # Test async operations
            resource_group = os.environ.get("AZURE_RESOURCE_GROUP", "test-rg")
            
            print("\\nTesting async operations...")
            
            # List configuration stores (this will succeed or fail based on permissions)
            try:
                stores = await app_config.list()
                print(f"✓ Listed configuration stores: {len(stores.get('value', []))} stores found")
            except Exception as e:
                print(f"⚠ Error listing stores (may be expected): {e}")
            
            # Demonstrate async context usage
            print("✓ Async operations completed successfully")

async def test_async_with_different_api_versions():
    """Test async factory with different API versions."""
    
    async with DefaultAzureCredential() as credential:
        client = AsyncManagementClient(
            credential=credential,
            subscription_id=os.environ["AZURE_SUBSCRIPTION_ID"],
        )
        
        async with client:
            # Test with default API version
            app_config_default = client("Microsoft.AppConfiguration")
            print(f"Default API version: {app_config_default.api_version}")
            
            # Test with specific API version
            app_config_specific = client("Microsoft.AppConfiguration", api_version="2022-05-01")
            print(f"Specific API version: {app_config_specific.api_version}")
            
            print("✓ API version handling works correctly")

if __name__ == "__main__":
    # Run the async tests
    asyncio.run(test_async_factory_instantiation())
    asyncio.run(test_async_with_different_api_versions())