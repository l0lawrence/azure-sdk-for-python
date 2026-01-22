# Azure packaging

[comment]: # ( cspell:ignore myservice )

This article describes the recommendations for defining namespace packaging to release a package inside the `azure` namespace. Being inside the `azure` namespace means that a service `myservice` can be imported using:
```python
import azure.myservice
```

Namespace packaging is complicated in Python, here's a few reading if you still doubt it:
- https://packaging.python.org/guides/packaging-namespace-packages/
- https://www.python.org/dev/peps/pep-0420/
- https://github.com/pypa/sample-namespace-packages

Note:
While this article provides an example using setup.py and an example using pyproject.toml, this can also be achieved with setup.cfg or other methods, as long as the constraints on the final wheels/sdist are met. For the purposes of this repository, we recommend using pyproject.toml.

*This page has been updated to be Python 3 only packages as we do not recommend supporting Python 2 after January 1st 2022.* If you still want to support Python 2 for some reasons, there is a section at the bottom with some details (or you have the Github history, to read the page as it was on November 1st 2021).

# What are the constraints?

We want to build sdist and wheels in order to follow the following constraints:
- Solution should work with *recent* versions of pip and setuptools (not the very latest only, but not archaeology either)
- Wheels must work with Python 3.9+
- mixed dev installation and PyPI installation should be explicitly addressed

# What do I do in my files to achieve that

The minimal files to have:
- azure/\_\_init\_\_.py
- MANIFEST.in
- pyproject.toml or setup.py

The file "azure/\_\_init\_\_.py" must contain exactly this:
```python
__path__ = __import__('pkgutil').extend_path(__path__, __name__)
```

Your MANIFEST.in must include the following line `include azure/__init__.py`.

Example:
```shell
include *.md
include LICENSE
include azure/__init__.py
recursive-include tests *.py
recursive-include samples *.py *.md
```
```
In your setup.py:

The "packages" section MUST EXCLUDE the `azure` package. Example:
```python
    packages=find_packages(exclude=[
        'tests',
        # Exclude packages that will be covered by PEP420 or nspkg
        'azure',
    ]),
```

Since the package is Python 3 only, you must notify it in the setup.py as well:
```python
    python_requires=">=3.9",
```
or in the pyproject.toml:
```python
    requires-python = ">=3.9",
```

Example of a full pyproject.toml
```python
[build-system]
requires = ["setuptools>=77.0.3", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "azure-eventhub"
authors = [
    {name = "Microsoft Corporation", email = "azpysdkhelp@microsoft.com"},
]
description = "Microsoft Azure Event Hubs Client Library for Python"
keywords = ["azure", "azure sdk"]
requires-python = ">=3.9"
license = "MIT"
classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
]
dependencies = [
    "azure-core>=1.27.0",
    "typing-extensions>=4.0.1",
]
dynamic = ["version", "readme"]

[project.urls]
repository = "https://github.com/Azure/azure-sdk-for-python/tree/main/sdk"

[tool.setuptools.dynamic]
version = {attr = "azure.eventhub._version.VERSION"}
readme = {file = ["README.md"], content-type = "text/markdown"}

[tool.setuptools.packages.find]
exclude = ["samples*", "tests*", "doc*", "stress*", "azure"]

[tool.setuptools.package-data]
pytyped = ["py.typed"]

[tool.azure-sdk-build]
pyright = false
type_check_samples = true
verifytypes = true
pylint = true
```

Example of a full setup.py
```python
#!/usr/bin/env python

#-------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#--------------------------------------------------------------------------

import re
import os.path
from io import open
from setuptools import find_packages, setup

# Change the PACKAGE_NAME only to change folder and different name
PACKAGE_NAME = "azure-keyvault"
PACKAGE_PPRINT_NAME = "KeyVault"

# a-b-c => a/b/c
package_folder_path = PACKAGE_NAME.replace('-', '/')
# a-b-c => a.b.c
namespace_name = PACKAGE_NAME.replace('-', '.')

# Version extraction inspired from 'requests'
with open(os.path.join(package_folder_path, 'version.py'), 'r') as fd:
    version = re.search(r'^VERSION\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

with open('README.rst', encoding='utf-8') as f:
    readme = f.read()
with open('HISTORY.rst', encoding='utf-8') as f:
    history = f.read()

setup(
    name=PACKAGE_NAME,
    version=version,
    description='Microsoft Azure {} Client Library for Python'.format(PACKAGE_PPRINT_NAME),
    long_description=readme + '\n\n' + history,
    license='MIT License',
    author='Microsoft Corporation',
    author_email='azpysdkhelp@microsoft.com',
    url='https://github.com/Azure/azure-sdk-for-python',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires=">=3.8",
    zip_safe=False,
    packages=find_packages(exclude=[
        'tests',
        # Exclude packages that will be covered by PEP420 or nspkg
        'azure',
    ]),
    install_requires=[
        'msrest>=0.5.0',
        'msrestazure>=0.4.32,<2.0.0',
        'azure-common~=1.1',
    ],
)
```

This syntax works with setuptools >= 24.2.0 (July 2016) and pip >= 9.0 (Nov 2016), which is considered enough to support in 2021.

Since the package is Python 3 only, do NOT make this wheel universal. This usually means you should NOT have `universal=1` in the `setup.cfg`. It may mean you can completely remove the file if `universal` was the only configuration option inside.

# How can I check if my packages are built correctly?

- wheel file must NOT contain a `azure/__init__.py` file (you can open it with a zip util to check)
- wheel file name suffix is `py3-none-any`, and NOT `py2.py3-none-any`.
- sdist must contain a `azure/__init__.py` file that declares `azure` as a namespace package using the `pkgutil` syntax