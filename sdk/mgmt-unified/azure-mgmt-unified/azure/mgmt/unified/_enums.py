# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Service type enumerations for Azure Management services."""

from enum import Enum


class ServiceType(str, Enum):
    """Enumeration of Azure Management Plane services.
    
    Each service corresponds to an azure-mgmt-* package and Azure Resource Provider.
    """
    
    # Core Management Services
    ADVISOR = "advisor"
    RESOURCE = "resource"
    SUBSCRIPTION = "subscription"
    
    # Compute Services
    COMPUTE = "compute"
    CONTAINER_INSTANCE = "containerinstance"
    CONTAINER_SERVICE = "containerservice"
    BATCH = "batch"
    
    # Storage Services
    STORAGE = "storage"
    STORAGE_CACHE = "storagecache"
    DATA_LAKE_STORE = "datalakestore"
    DATA_LAKE_ANALYTICS = "datalakeanalytics"
    
    # Networking Services
    NETWORK = "network"
    DNS = "dns"
    TRAFFIC_MANAGER = "trafficmanager"
    CDN = "cdn"
    FRONT_DOOR = "frontdoor"
    
    # Database Services
    SQL = "sql"
    COSMOSDB = "cosmosdb"
    REDIS = "redis"
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    MARIADB = "mariadb"
    
    # Analytics Services
    SYNAPSE = "synapse"
    DATABRICKS = "databricks"
    HDI = "hdinsight"
    DATA_FACTORY = "datafactory"
    STREAM_ANALYTICS = "streamanalytics"
    
    # AI + Machine Learning
    COGNITIVE_SERVICES = "cognitiveservices"
    MACHINE_LEARNING = "machinelearning"
    BOT_SERVICE = "botservice"
    
    # Application Services
    APP_SERVICE = "appservice"
    APP_CONFIGURATION = "appconfiguration"
    CONTAINER_APPS = "containerapps"
    SERVICE_BUS = "servicebus"
    EVENT_HUB = "eventhub"
    EVENT_GRID = "eventgrid"
    NOTIFICATION_HUBS = "notificationhubs"
    SIGNALR = "signalr"
    
    # Security & Identity
    KEY_VAULT = "keyvault"
    MANAGED_IDENTITY = "managedidentity"
    AUTHORIZATION = "authorization"
    SECURITY = "security"
    
    # Monitoring & Management
    MONITOR = "monitor"
    APPLICATION_INSIGHTS = "applicationinsights"
    LOG_ANALYTICS = "loganalytics"
    AUTOMATION = "automation"
    
    # IoT Services
    IOT_HUB = "iothub"
    IOT_CENTRAL = "iotcentral"
    DIGITAL_TWINS = "digitaltwins"
    
    # Integration Services
    LOGIC_APPS = "logic"
    API_MANAGEMENT = "apimanagement"
    SERVICE_BUS_RELAY = "relay"
    
    # Media Services
    MEDIA_SERVICES = "media"
    
    # Developer Tools
    DEV_TEST_LABS = "devtestlabs"
    DEPLOYMENT_MANAGER = "deploymentmanager"
    
    @property
    def resource_provider(self) -> str:
        """Get the Azure Resource Provider name for this service.
        
        Returns:
            The Microsoft.* resource provider name.
        """
        from ._service_registry import SERVICE_REGISTRY
        return SERVICE_REGISTRY[self]["resource_provider"]
    
    @property
    def package_name(self) -> str:
        """Get the azure-mgmt-* package name for this service.
        
        Returns:
            The package name (e.g., 'azure.mgmt.storage').
        """
        from ._service_registry import SERVICE_REGISTRY
        return SERVICE_REGISTRY[self]["package"]
    
    @property
    def default_api_version(self) -> str:
        """Get the default API version for this service.
        
        Returns:
            The default API version string.
        """
        from ._service_registry import SERVICE_REGISTRY
        return SERVICE_REGISTRY[self]["default_api_version"]
