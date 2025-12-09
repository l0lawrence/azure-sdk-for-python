# Service Registry Pattern (Generalized)

This note captures the pattern used in `azure_mgmt_appconfiguration.py` so it can be reused across SDK factories.

## Core Concepts
- **Factory per provider**: Each resource provider gets a `ServiceProviderFactory`-derived class (e.g., `AppConfigurationFactory`), constructed with `ManagementClient`, `service_provider`, optional `subscription_id`, and `api_version`.
- **Route maps**:
  - `routes_by_method: Dict[str, Dict[str, Callable[..., Any]]]` stores per-verb lambdas that build relative URLs and delegate to `get/post/put/patch/delete`.
  - `operations_by_group: TypedDict` maps operation-group names to protocol-typed views (e.g., `configuration_stores`, `key_values`, `replicas`, `snapshots`).
  - `operations_by_method` is a typing convenience for verb protocols; user guidance favors group access and concrete methods.
- **Protocols for typing**: Module-level `Protocol` classes define each group surface (e.g., `ConfigurationStoresOperations`) and verb-specific protocols. Implementations live on the factory; protocols drive IntelliSense and type checking.
- **Concrete methods**: The factory implements public methods (e.g., `list`, `begin_create`, `get_replica`, `begin_create_snapshot`) that forward to `routes_by_method` and return typed results.
- **Dynamic dispatch**: `__getattr__` falls back to `routes_by_method`; `_call_route` centralizes lookup and raises `AttributeError` for unknown operations. This allows calling any route entry even without a dedicated wrapper.
- **LRO handling**: All `begin_*` routes wrap the HTTP response with `_create_lro_poller`, ensuring callers get `LROPoller` rather than raw `HttpResponse`.
- **Base HTTP helpers**: `ServiceProviderFactory` provides `get/post/put/patch/delete` that prepend the provider base URL, append `api-version`, build `HttpRequest`, set body (`model/json/data`), and send via the shared ARM pipeline.

## How to Extend to a New Provider/SDK
1. Define operation-group `Protocol`s and an `OperationsByGroup` `TypedDict`.
2. Add `routes_by_method` entries for each operation (URL templates + verb).
3. Rely on `__getattr__` for dynamic implementation; keep public surface consistent with the protocols.
4. Ensure all `begin_*` entries use `_create_lro_poller` so LROs return pollers.
5. Wire `operations_by_group` casts in `__init__`; keep `operations_by_method` for typing parity if desired.

## Notes
- This pattern is provider-agnostic and can be reused across sync/async variants with analogous route maps and dispatch.
- Keep URL construction and api-version handling in the base factory helpers to avoid duplication.
