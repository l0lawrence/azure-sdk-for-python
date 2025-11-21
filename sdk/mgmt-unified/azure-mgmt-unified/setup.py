#!/usr/bin/env python

#-------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#--------------------------------------------------------------------------

import os
from setuptools import setup, find_packages

# azure v0.x is not compatible with this package
# azure v0.x used to have a __version__ attribute (newer versions don't)
try:
    import azure
    try:
        ver = azure.__version__
        raise Exception(
            'This package is incompatible with azure=={}. '.format(ver) +
            'Uninstall it with "pip uninstall azure".'
        )
    except AttributeError:
        pass
except ImportError:
    pass

setup(
    name='azure-mgmt-unified',
    version='1.0.0b1',
    description='Unified Azure Management Plane Client Library for Python',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    license='MIT License',
    author='Microsoft Corporation',
    author_email='azpysdkhelp@microsoft.com',
    url='https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/mgmt-unified/azure-mgmt-unified',
    keywords='azure, azure sdk',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
    ],
    zip_safe=False,
    packages=find_packages(exclude=[
        'tests',
        'tests.*',
    ]),
    python_requires='>=3.8',
    install_requires=[
        'azure-core>=1.30.0',
        'azure-mgmt-core>=1.6.0',
        'typing-extensions>=4.6.0',
        'msrest>=0.7.1',
    ],
    extras_require={
        'advisor': ['azure-mgmt-advisor>=9.0.0'],
        'storage': ['azure-mgmt-storage>=21.0.0'],
        'compute': ['azure-mgmt-compute>=30.0.0'],
        'network': ['azure-mgmt-network>=25.0.0'],
        'all': [
            'azure-mgmt-advisor>=9.0.0',
            'azure-mgmt-storage>=21.0.0',
            'azure-mgmt-compute>=30.0.0',
            'azure-mgmt-network>=25.0.0',
        ],
    },
)
