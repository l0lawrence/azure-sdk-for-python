#!/usr/bin/env python

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
Example: Basic usage of UnifiedManagementClient

This example demonstrates:
1. Creating a multi-service unified client
2. Listing resources from different services
3. Using service-scoped clients
4. Custom API version configuration
"""

import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.unified import UnifiedManagementClient, ServiceType


def example_multi_service_client():
    """Example: Multi-service client with automatic service detection."""
    print("=" * 60)
    print("Example 1: Multi-Service Client")
    print("=" * 60)
    
    # Get credentials and subscription ID from environment
    credential = DefaultAzureCredential()
    subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
    
    if not subscription_id:
        print("⚠️  AZURE_SUBSCRIPTION_ID environment variable not set")
        print("   Set it with: $env:AZURE_SUBSCRIPTION_ID='your-subscription-id'")
        return
    
    # Create unified client (multi-service)
    print(f"\n✓ Creating unified client for subscription: {subscription_id[:8]}...")
    client = UnifiedManagementClient(credential, subscription_id)
    print(f"  Client: {client}")
    
    # Access different services - automatic service detection
    print("\n1. Listing storage accounts (from Storage service)...")
    try:
        storage_accounts = client.storage_accounts.list()
        count = 0
        for account in storage_accounts:
            print(f"   - {account.name} ({account.location})")
            count += 1
            if count >= 3:  # Limit output
                print("   ...")
                break
        if count == 0:
            print("   No storage accounts found")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n2. Listing recommendations (from Advisor service)...")
    try:
        recommendations = client.recommendations.list()
        count = 0
        for rec in recommendations:
            print(f"   - {rec.name}: {rec.short_description.problem if hasattr(rec, 'short_description') else 'N/A'}")
            count += 1
            if count >= 3:
                print("   ...")
                break
        if count == 0:
            print("   No recommendations found")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Clean up
    client.close()
    print("\n✓ Client closed")


def example_service_scoped_client():
    """Example: Service-scoped client for specific service."""
    print("\n" + "=" * 60)
    print("Example 2: Service-Scoped Client")
    print("=" * 60)
    
    credential = DefaultAzureCredential()
    subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
    
    if not subscription_id:
        print("⚠️  AZURE_SUBSCRIPTION_ID not set")
        return
    
    # Create service-scoped client for Storage
    print(f"\n✓ Creating storage-scoped client...")
    storage_client = UnifiedManagementClient(
        credential,
        subscription_id,
        service=ServiceType.STORAGE
    )
    print(f"  Client: {storage_client}")
    
    # All operations route to storage service
    print("\n1. Listing storage accounts...")
    try:
        accounts = storage_client.storage_accounts.list()
        count = sum(1 for _ in accounts)
        print(f"   Found {count} storage accounts")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n2. Listing blob services...")
    try:
        # This also routes to storage service
        services = storage_client.operations.list()
        print(f"   ✓ Operations available")
    except Exception as e:
        print(f"   Error: {e}")
    
    storage_client.close()
    print("\n✓ Client closed")


def example_custom_api_versions():
    """Example: Custom API versions per service."""
    print("\n" + "=" * 60)
    print("Example 3: Custom API Versions")
    print("=" * 60)
    
    credential = DefaultAzureCredential()
    subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
    
    if not subscription_id:
        print("⚠️  AZURE_SUBSCRIPTION_ID not set")
        return
    
    # Create client with custom API versions
    print("\n✓ Creating client with custom API versions...")
    client = UnifiedManagementClient(
        credential,
        subscription_id,
        api_versions={
            ServiceType.STORAGE: "2022-09-01",  # Override default
            ServiceType.ADVISOR: "2020-01-01",  # Use specific version
        }
    )
    
    print(f"  Storage API version: {client._api_versions.get(ServiceType.STORAGE)}")
    print(f"  Advisor API version: {client._api_versions.get(ServiceType.ADVISOR)}")
    print(f"  Compute API version: {client._api_versions.get(ServiceType.COMPUTE)} (default)")
    
    client.close()
    print("\n✓ Client closed")


def example_context_manager():
    """Example: Using client as context manager."""
    print("\n" + "=" * 60)
    print("Example 4: Context Manager")
    print("=" * 60)
    
    credential = DefaultAzureCredential()
    subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
    
    if not subscription_id:
        print("⚠️  AZURE_SUBSCRIPTION_ID not set")
        return
    
    # Use with context manager for automatic cleanup
    print("\n✓ Using client with context manager...")
    with UnifiedManagementClient(credential, subscription_id) as client:
        print(f"  Client: {client}")
        
        try:
            # Use the client
            operations = client.operations.list()
            print("  ✓ Operations listed successfully")
        except Exception as e:
            print(f"  Error: {e}")
    
    print("✓ Client automatically closed")


def example_direct_service_access():
    """Example: Direct access to underlying service clients."""
    print("\n" + "=" * 60)
    print("Example 5: Direct Service Client Access")
    print("=" * 60)
    
    credential = DefaultAzureCredential()
    subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
    
    if not subscription_id:
        print("⚠️  AZURE_SUBSCRIPTION_ID not set")
        return
    
    print("\n✓ Creating unified client...")
    with UnifiedManagementClient(credential, subscription_id) as client:
        # Get direct access to underlying StorageManagementClient
        print("\n1. Getting direct access to StorageManagementClient...")
        try:
            storage_client = client.get_service_client(ServiceType.STORAGE)
            print(f"   Storage client type: {type(storage_client).__name__}")
            print(f"   Has storage_accounts: {hasattr(storage_client, 'storage_accounts')}")
        except ImportError:
            print("   ⚠️  azure-mgmt-storage not installed")
            print("      Install with: pip install azure-mgmt-unified[storage]")
        except Exception as e:
            print(f"   Error: {e}")
        
        print("\n2. Getting direct access to AdvisorManagementClient...")
        try:
            advisor_client = client.get_service_client(ServiceType.ADVISOR)
            print(f"   Advisor client type: {type(advisor_client).__name__}")
            print(f"   Has recommendations: {hasattr(advisor_client, 'recommendations')}")
        except ImportError:
            print("   ⚠️  azure-mgmt-advisor not installed")
            print("      Install with: pip install azure-mgmt-unified[advisor]")
        except Exception as e:
            print(f"   Error: {e}")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("Azure Unified Management Client - Examples")
    print("=" * 60)
    print("\nThese examples demonstrate the unified management client")
    print("that provides access to multiple Azure services through")
    print("a single client interface.\n")
    
    # Check prerequisites
    subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
    if not subscription_id:
        print("⚠️  Prerequisites:")
        print("   1. Set AZURE_SUBSCRIPTION_ID environment variable")
        print("      PowerShell: $env:AZURE_SUBSCRIPTION_ID='your-subscription-id'")
        print("   2. Authenticate with Azure:")
        print("      az login")
        print("   3. Install optional service packages:")
        print("      pip install azure-mgmt-unified[storage,advisor,compute]")
        print("\n")
    
    try:
        # Run examples
        example_multi_service_client()
        example_service_scoped_client()
        example_custom_api_versions()
        example_context_manager()
        example_direct_service_access()
        
        print("\n" + "=" * 60)
        print("✓ All examples completed")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Examples interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
