# Quick Start: TypeSpec SDK Generation

This guide provides a quick start for generating Azure SDKs for Python using TypeSpec.

## Prerequisites

1. Install the `uv` package manager (Python)
2. Authenticate with GitHub CLI:
   ```bash
   gh auth login
   ```

## Getting Started

1. Clone the [azure-sdk-for-python](https://github.com/Azure/azure-sdk-for-python) repo

2. Create a feature branch:
   ```bash
   git checkout -b your-feature-branch
   ```

3. Open VS Code GitHub Copilot. Select agent mode and choose any model.

4. **Start the Generation**
   - Have your `tspconfig.yaml` path ready (local or remote URL)
   - Send any of these example prompts to the Copilot:
     - "Generate SDK from my TypeSpec at `<path/to/tspconfig.yaml>`"
     - "Generate SDK from TypeSpec at `<URL_to_tspconfig.yaml>`"

5. **Follow the Process**
   - Environment verification (1-2 minutes)
   - SDK generation (5-6 minutes)
   - Validation and fixes (3-5 minutes per validation step)
   - Documentation updates
   - Commit and PR creation

## What to Expect

1. **Duration**: Full process takes ~15-20 minutes
2. **Automatic Steps**:
   - Environment checks
   - SDK generation
   - Code validation
   - Documentation updates
   - PR creation

3. **Your Input Needed For**:
   - Confirming file changes
   - Reviewing commit messages
   - Providing changelog entries

## Next Steps

After generation completes, you'll be prompted to use the azure-rest-api-specs agent with your new PR for further processing.
