
# Operations List for AppConfig


Configuration Stores
- def list(self, skip_token: Optional[str] = None, **kwargs: Any) -> ItemPaged["_models.ConfigurationStore"]:
- def list_by_resource_group(
        self, resource_group_name: str, skip_token: Optional[str] = None, **kwargs: Any
    ) -> ItemPaged["_models.ConfigurationStore"]:
-     def get(self, resource_group_name: str, config_store_name: str, **kwargs: Any) -> _models.ConfigurationStore:
-  def begin_create(
        self,
        resource_group_name: str,
        config_store_name: str,
        config_store_creation_parameters: Union[_models.ConfigurationStore, IO[bytes]],
        **kwargs: Any
    ) -> LROPoller[_models.ConfigurationStore]:
-     def begin_delete(self, resource_group_name: str, config_store_name: str, **kwargs: Any) -> LROPoller[None]:
-     def begin_update(
        self,
        resource_group_name: str,
        config_store_name: str,
        config_store_update_parameters: Union[_models.ConfigurationStoreUpdateParameters, IO[bytes]],
        **kwargs: Any
    ) -> LROPoller[_models.ConfigurationStore]:
-     def list_keys(
        self, resource_group_name: str, config_store_name: str, skip_token: Optional[str] = None, **kwargs: Any
    ) -> ItemPaged["_models.ApiKey"]:

-     def regenerate_key(
        self,
        resource_group_name: str,
        config_store_name: str,
        regenerate_key_parameters: Union[_models.RegenerateKeyParameters, IO[bytes]],
        **kwargs: Any
    ) -> _models.ApiKey:
-  def list_deleted(self, **kwargs: Any) -> ItemPaged["_models.DeletedConfigurationStore"]:
- def get_deleted(self, location: str, config_store_name: str, **kwargs: Any) -> _models.DeletedConfigurationStore:
-     def begin_purge_deleted(self, location: str, config_store_name: str, **kwargs: Any) -> LROPoller[None]:
- 

KeyValues Operations
-     def get(
        self, resource_group_name: str, config_store_name: str, key_value_name: str, **kwargs: Any
    ) -> _models.KeyValue:
-     def create_or_update(
        self,
        resource_group_name: str,
        config_store_name: str,
        key_value_name: str,
        key_value_parameters: Union[_models.KeyValue, IO[bytes]],
        **kwargs: Any
    ) -> _models.KeyValue:
-     def begin_delete(
        self, resource_group_name: str, config_store_name: str, key_value_name: str, **kwargs: Any
    ) -> LROPoller[None]:

Operations

-     def check_name_availability(
        self,
        check_name_availability_parameters: Union[_models.CheckNameAvailabilityParameters, IO[bytes]],
        **kwargs: Any
    ) -> _models.NameAvailabilityStatus:
-     def list(self, skip_token: Optional[str] = None, **kwargs: Any) -> ItemPaged["_models.OperationDefinition"]:  (list all operations available)
-     def regional_check_name_availability(
        self,
        location: str,
        check_name_availability_parameters: Union[_models.CheckNameAvailabilityParameters, IO[bytes]],
        **kwargs: Any
    ) -> _models.NameAvailabilityStatus:


Private Endpoint Connections
-     def list_by_configuration_store(
        self, resource_group_name: str, config_store_name: str, **kwargs: Any
    ) -> ItemPaged["_models.PrivateEndpointConnection"]:
-     def get(
        self, resource_group_name: str, config_store_name: str, private_endpoint_connection_name: str, **kwargs: Any
    ) -> _models.PrivateEndpointConnection:
-     def begin_create_or_update(
        self,
        resource_group_name: str,
        config_store_name: str,
        private_endpoint_connection_name: str,
        private_endpoint_connection: Union[_models.PrivateEndpointConnection, IO[bytes]],
        **kwargs: Any
    ) -> LROPoller[_models.PrivateEndpointConnection]:
-     def begin_delete(
        self, resource_group_name: str, config_store_name: str, private_endpoint_connection_name: str, **kwargs: Any
    ) -> LROPoller[None]:

Private Link Resources Operations
-     def list_by_configuration_store(
        self, resource_group_name: str, config_store_name: str, **kwargs: Any
    ) -> ItemPaged["_models.PrivateLinkResource"]:
-     def get(
        self, resource_group_name: str, config_store_name: str, group_name: str, **kwargs: Any
    ) -> _models.PrivateLinkResource:

Replicas Operations
-     def list_by_configuration_store(
        self, resource_group_name: str, config_store_name: str, skip_token: Optional[str] = None, **kwargs: Any
    ) -> ItemPaged["_models.Replica"]:
-     def get(
        self, resource_group_name: str, config_store_name: str, replica_name: str, **kwargs: Any
    ) -> _models.Replica:
-     def begin_create(
        self,
        resource_group_name: str,
        config_store_name: str,
        replica_name: str,
        replica_creation_parameters: Union[_models.Replica, IO[bytes]],
        **kwargs: Any
    ) -> LROPoller[_models.Replica]:
-     def begin_delete(
        self, resource_group_name: str, config_store_name: str, replica_name: str, **kwargs: Any
    ) -> LROPoller[None]:

Snapshots Operations

    def get(
        self, resource_group_name: str, config_store_name: str, snapshot_name: str, **kwargs: Any
    ) -> _models.Snapshot:

        def begin_create(
        self,
        resource_group_name: str,
        config_store_name: str,
        snapshot_name: str,
        body: Union[_models.Snapshot, IO[bytes]],
        **kwargs: Any
    ) -> LROPoller[_models.Snapshot]:
