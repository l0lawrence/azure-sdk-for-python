# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
Unified Azure Management Plane Client Library for Python

This package provides a unified interface to Azure Management Plane services.
"""

from ._version import VERSION
from ._client import UnifiedManagementClient
from ._enums import ServiceType
from ._models import ResourceBase, ResourceListResult

__version__ = VERSION

__all__ = [
    "UnifiedManagementClient",
    "ServiceType",
    "ResourceBase",
    "ResourceListResult",
]
