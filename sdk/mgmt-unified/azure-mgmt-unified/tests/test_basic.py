#!/usr/bin/env python

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Basic tests for unified management client."""

import unittest
from unittest.mock import Mock, MagicMock, patch
from azure.mgmt.unified import UnifiedManagementClient, ServiceType
from azure.mgmt.unified._api_versions import ServiceAPIVersions
from azure.mgmt.unified._service_registry import get_service_for_operation


class TestServiceAPIVersions(unittest.TestCase):
    """Tests for ServiceAPIVersions class."""
    
    def test_default_versions(self):
        """Test that default versions are loaded."""
        api_versions = ServiceAPIVersions()
        
        # Check some known services have default versions
        self.assertIsNotNone(api_versions.get(ServiceType.STORAGE))
        self.assertIsNotNone(api_versions.get(ServiceType.ADVISOR))
        self.assertIsNotNone(api_versions.get(ServiceType.COMPUTE))
    
    def test_custom_versions(self):
        """Test that custom versions override defaults."""
        custom_versions = {
            ServiceType.STORAGE: "2022-01-01",
            ServiceType.COMPUTE: "2023-01-01",
        }
        api_versions = ServiceAPIVersions(custom_versions)
        
        # Check custom versions are used
        self.assertEqual(api_versions.get(ServiceType.STORAGE), "2022-01-01")
        self.assertEqual(api_versions.get(ServiceType.COMPUTE), "2023-01-01")
        
        # Check default version is used for non-overridden services
        default_advisor = api_versions.get_default(ServiceType.ADVISOR)
        self.assertEqual(api_versions.get(ServiceType.ADVISOR), default_advisor)
    
    def test_is_custom(self):
        """Test checking if a version is custom."""
        custom_versions = {ServiceType.STORAGE: "2022-01-01"}
        api_versions = ServiceAPIVersions(custom_versions)
        
        self.assertTrue(api_versions.is_custom(ServiceType.STORAGE))
        self.assertFalse(api_versions.is_custom(ServiceType.ADVISOR))
    
    def test_set_and_reset(self):
        """Test setting and resetting API versions."""
        api_versions = ServiceAPIVersions()
        
        # Get default
        default_version = api_versions.get(ServiceType.STORAGE)
        
        # Set custom
        api_versions.set(ServiceType.STORAGE, "2020-01-01")
        self.assertEqual(api_versions.get(ServiceType.STORAGE), "2020-01-01")
        self.assertTrue(api_versions.is_custom(ServiceType.STORAGE))
        
        # Reset to default
        api_versions.reset(ServiceType.STORAGE)
        self.assertEqual(api_versions.get(ServiceType.STORAGE), default_version)
        self.assertFalse(api_versions.is_custom(ServiceType.STORAGE))


class TestServiceRegistry(unittest.TestCase):
    """Tests for service registry functionality."""
    
    def test_get_service_for_operation(self):
        """Test operation to service mapping."""
        # Test known operations
        self.assertEqual(get_service_for_operation("storage_accounts"), ServiceType.STORAGE)
        self.assertEqual(get_service_for_operation("recommendations"), ServiceType.ADVISOR)
        self.assertEqual(get_service_for_operation("virtual_machines"), ServiceType.COMPUTE)
    
    def test_get_service_for_unknown_operation(self):
        """Test that unknown operations raise KeyError."""
        with self.assertRaises(KeyError):
            get_service_for_operation("unknown_operation_xyz")


class TestUnifiedManagementClient(unittest.TestCase):
    """Tests for UnifiedManagementClient."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_credential = Mock()
        self.subscription_id = "00000000-0000-0000-0000-000000000000"
    
    def test_client_initialization(self):
        """Test client initializes correctly."""
        client = UnifiedManagementClient(self.mock_credential, self.subscription_id)
        
        self.assertEqual(client._subscription_id, self.subscription_id)
        self.assertIsNone(client._service)
        self.assertIsInstance(client._api_versions, ServiceAPIVersions)
        self.assertEqual(len(client._service_clients), 0)  # No clients loaded yet
        
        client.close()
    
    def test_service_scoped_client(self):
        """Test service-scoped client initialization."""
        client = UnifiedManagementClient(
            self.mock_credential,
            self.subscription_id,
            service=ServiceType.STORAGE
        )
        
        self.assertEqual(client._service, ServiceType.STORAGE)
        client.close()
    
    def test_custom_api_versions(self):
        """Test client with custom API versions."""
        custom_versions = {ServiceType.STORAGE: "2022-01-01"}
        client = UnifiedManagementClient(
            self.mock_credential,
            self.subscription_id,
            api_versions=custom_versions
        )
        
        self.assertEqual(
            client._api_versions.get(ServiceType.STORAGE),
            "2022-01-01"
        )
        client.close()
    
    def test_context_manager(self):
        """Test client as context manager."""
        with UnifiedManagementClient(self.mock_credential, self.subscription_id) as client:
            self.assertIsNotNone(client)
        # Client should be closed after exiting context
    
    def test_repr(self):
        """Test string representation."""
        client = UnifiedManagementClient(self.mock_credential, self.subscription_id)
        repr_str = repr(client)
        
        self.assertIn("UnifiedManagementClient", repr_str)
        self.assertIn("multi-service", repr_str)
        
        client.close()
        
        # Test service-scoped repr
        client = UnifiedManagementClient(
            self.mock_credential,
            self.subscription_id,
            service=ServiceType.STORAGE
        )
        repr_str = repr(client)
        
        self.assertIn("service=storage", repr_str)
        client.close()


class TestServiceType(unittest.TestCase):
    """Tests for ServiceType enum."""
    
    def test_resource_provider_property(self):
        """Test resource provider property."""
        self.assertEqual(ServiceType.STORAGE.resource_provider, "Microsoft.Storage")
        self.assertEqual(ServiceType.COMPUTE.resource_provider, "Microsoft.Compute")
        self.assertEqual(ServiceType.ADVISOR.resource_provider, "Microsoft.Advisor")
    
    def test_package_name_property(self):
        """Test package name property."""
        self.assertEqual(ServiceType.STORAGE.package_name, "azure.mgmt.storage")
        self.assertEqual(ServiceType.COMPUTE.package_name, "azure.mgmt.compute")
        self.assertEqual(ServiceType.ADVISOR.package_name, "azure.mgmt.advisor")
    
    def test_default_api_version_property(self):
        """Test default API version property."""
        # Just check they return strings
        self.assertIsInstance(ServiceType.STORAGE.default_api_version, str)
        self.assertIsInstance(ServiceType.COMPUTE.default_api_version, str)


def run_tests():
    """Run all tests."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestServiceAPIVersions))
    suite.addTests(loader.loadTestsFromTestCase(TestServiceRegistry))
    suite.addTests(loader.loadTestsFromTestCase(TestUnifiedManagementClient))
    suite.addTests(loader.loadTestsFromTestCase(TestServiceType))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    import sys
    success = run_tests()
    sys.exit(0 if success else 1)
