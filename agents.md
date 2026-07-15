# GitHub Copilot Agent Guide for Azure SDK for Python CI Fixes

This document provides guidance for using GitHub Copilot's coding agent to automatically fix CI (Continuous Integration) issues in your pull requests for the Azure SDK for Python repository.

## Overview

When your PR fails CI checks, you can use GitHub Copilot's coding agent (@copilot) to automatically identify and fix the issues. The coding agent can analyze error logs, understand the repository's code standards, and generate fixes for most common CI failures.

## How to Use the Coding Agent for CI Fixes

### Step 1: Identify the Failed Check

When a CI check fails on your PR, you'll see a red ❌ next to the check name. Common failed checks include:
- **Analyze** - Static analysis (linting, type checking, formatting)
- **Build** - Package building and installation
- **Test** - Unit and integration tests
- **Check Enforcer** - Ensures all required checks pass

### Step 2: Request a Fix from Copilot

You can ask Copilot to fix CI issues in several ways:

#### Option A: Ask Copilot to Analyze the Failure
```
@copilot The Analyze check failed on my PR. Can you look at the error logs and fix the issues?
```

#### Option B: Be Specific About the Check Type
```
@copilot The pylint check is failing with several issues. Please fix the linting errors in my code.
```

```
@copilot MyPy is reporting type errors. Can you add the correct type annotations?
```

```
@copilot The black formatter check failed. Please format my code to match the repository standards.
```

#### Option C: Paste the Error Message
If you have specific errors, paste them:
```
@copilot I'm getting this error in CI:

sdk/myservice/azure-myservice/azure/myservice/_client.py:45:0: C0301: Line too long (125/120) (line-too-long)
sdk/myservice/azure-myservice/azure/myservice/_client.py:67:4: C0116: Missing function or method docstring (missing-function-docstring)

Can you fix these issues?
```

## Common CI Failures and How to Ask Copilot to Fix Them

### 1. Pylint Failures (Code Linting)

**Symptoms:**
- Line too long errors
- Missing docstrings
- Unused imports
- Naming convention violations

**How to ask Copilot:**
```
@copilot Fix the pylint errors in my PR. The issues are:
- Lines too long in _client.py
- Missing docstrings in several functions
- Unused import statements
```

**What Copilot will do:**
- Reformat long lines to be under 120 characters
- Add appropriate docstrings following Azure SDK standards
- Remove unused imports
- Fix naming convention issues

### 2. MyPy/Pyright Failures (Type Checking)

**Symptoms:**
- Missing type hints
- Incorrect return types
- Type mismatches
- Incompatible argument types

**How to ask Copilot:**
```
@copilot The MyPy check is failing because of missing type annotations. Please add proper type hints to my code following the repository's typing standards.
```

**What Copilot will do:**
- Add type annotations to function parameters and return values
- Fix type mismatches
- Import necessary typing modules (List, Dict, Optional, etc.)
- Ensure type completeness

### 3. Black Formatting Failures

**Symptoms:**
- Inconsistent code formatting
- Wrong indentation
- Incorrect line breaks

**How to ask Copilot:**
```
@copilot The black formatter check failed. Please reformat my code to match the repository's formatting standards.
```

**What Copilot will do:**
- Reformat all Python files using black's configuration
- Fix indentation and line breaks
- Ensure consistent quote usage
- Apply proper spacing

### 4. Sphinx/Documentation Failures

**Symptoms:**
- Malformed docstrings
- Invalid reStructuredText syntax
- Missing parameter documentation
- Broken references

**How to ask Copilot:**
```
@copilot The Sphinx documentation build is failing. Can you fix the docstring errors and ensure all public methods are properly documented?
```

**What Copilot will do:**
- Fix reStructuredText syntax in docstrings
- Add missing parameter and return value documentation
- Ensure docstrings follow Azure SDK documentation standards
- Fix broken cross-references

### 5. Import and Build Failures

**Symptoms:**
- Module not found errors
- Missing `__init__.py` files
- Import errors
- Circular import issues

**How to ask Copilot:**
```
@copilot My build is failing with import errors. Can you check the package structure and fix any missing __init__.py files or import issues?
```

**What Copilot will do:**
- Add missing `__init__.py` files
- Fix import statements
- Update `MANIFEST.in` if needed
- Resolve circular dependencies

### 6. Test Failures

**Symptoms:**
- Test assertions failing
- Missing test fixtures
- Incorrect mock configurations
- Recording/playback issues

**How to ask Copilot:**
```
@copilot Several tests are failing in test_client.py. Here's the error:

AssertionError: Expected status code 200 but got 404

Can you fix the test?
```

**What Copilot will do:**
- Analyze test failures and fix assertions
- Update test mocks and fixtures
- Fix test setup and teardown
- Ensure tests follow repository patterns

### 7. Bandit Security Issues

**Symptoms:**
- Security warnings in code
- Hardcoded passwords or secrets
- Unsafe use of eval/exec
- SQL injection risks

**How to ask Copilot:**
```
@copilot Bandit is reporting security issues in my code. Can you fix these security vulnerabilities?
```

**What Copilot will do:**
- Remove hardcoded secrets and suggest environment variables
- Replace unsafe patterns with secure alternatives
- Add appropriate security comments where needed
- Follow security best practices

## Advanced: Fixing Multiple Issues at Once

If you have multiple CI failures, you can ask Copilot to fix them all:

```
@copilot My PR has failed the following CI checks:
1. Pylint - line too long errors and missing docstrings
2. MyPy - missing type annotations
3. Black - formatting issues

Can you create a PR to fix all of these issues?
```

## Best Practices for Working with the Coding Agent

### 1. Provide Context
Include relevant error messages and file names:
```
@copilot Fix the pylint errors in sdk/keyvault/azure-keyvault-secrets/azure/keyvault/secrets/_client.py
```

### 2. Reference the CI Log
If the error is complex, copy the relevant part of the CI log:
```
@copilot Here's the CI error I'm getting:

[paste error log here]

Can you fix this?
```

### 3. Ask for Explanations
If you want to understand the fix:
```
@copilot Fix the MyPy errors and explain what type annotations were missing and why they're needed.
```

### 4. Iterate if Needed
If the first fix doesn't work:
```
@copilot The fix you suggested didn't resolve the issue. The CI is still failing with this error: [paste error]. Can you try a different approach?
```

### 5. Verify Before Merging
Always ask Copilot to explain what it changed:
```
@copilot Can you summarize the changes you made to fix the CI issues?
```

## Example Workflows

### Workflow 1: Complete CI Fix
```
Developer: @copilot My PR failed the Analyze check. Here are the errors:
- Pylint: 5 issues in _client.py
- MyPy: 3 type annotation issues  
- Black: formatting issues in 2 files

Can you fix all of these?

Copilot: [Creates PR with fixes]

Developer: @copilot Can you explain what you changed?

Copilot: [Provides summary of changes]
```

### Workflow 2: Iterative Fixing
```
Developer: @copilot Fix the test failures in my PR

Copilot: [Attempts fix]

Developer: @copilot That fix helped but there's still one failing test. Here's the new error: [paste error]

Copilot: [Provides updated fix]
```

### Workflow 3: Preventive Fixing
```
Developer: @copilot Before I submit my PR, can you check if my code will pass the CI checks for:
- Pylint
- MyPy
- Black formatting

And fix any issues you find?

Copilot: [Analyzes and fixes issues proactively]
```

## Understanding What Copilot Can and Cannot Fix

### ✅ Copilot Can Fix:
- Code formatting issues (black, line length)
- Linting errors (pylint violations)
- Type annotation errors (mypy, pyright)
- Missing docstrings
- Import statement issues
- Simple test assertion fixes
- Security warnings (bandit)
- Documentation build errors

### ⚠️ Copilot May Need Help With:
- Complex test failures requiring domain knowledge
- API design decisions
- Breaking changes that need architectural discussion
- Integration test failures requiring live Azure resources
- Performance issues

### ❌ Copilot Cannot Fix:
- Infrastructure or pipeline configuration issues
- Azure DevOps pipeline failures (non-code issues)
- Network or environment-specific failures
- Issues requiring Azure resource access

## Tips for Success

1. **Be Specific**: The more specific your request, the better the fix
2. **Include Errors**: Always paste relevant error messages
3. **One Issue at a Time**: For complex issues, break them down
4. **Review Changes**: Always review Copilot's changes before merging
5. **Provide Feedback**: If a fix doesn't work, tell Copilot and it will try again

## Troubleshooting Copilot Fixes

### If Copilot's Fix Doesn't Work:

1. **Provide More Context**:
```
@copilot The fix didn't work. Here's the complete error message and the relevant code section: [paste]
```

2. **Ask for Alternative Approaches**:
```
@copilot That approach didn't solve the issue. Can you try a different way to fix this?
```

3. **Request Explanation**:
```
@copilot Can you explain why you made these changes so I can better understand the issue?
```

4. **Check Related Files**:
```
@copilot The error might be related to other files. Can you check imports and dependencies?
```

## Quick Reference Commands

| CI Failure Type | Command to Fix |
|----------------|----------------|
| Pylint errors | `@copilot Fix the pylint errors in my PR` |
| Type checking (MyPy) | `@copilot Add missing type annotations to fix MyPy errors` |
| Formatting (Black) | `@copilot Reformat my code to pass the black formatter check` |
| Documentation (Sphinx) | `@copilot Fix the docstring errors causing Sphinx to fail` |
| Security (Bandit) | `@copilot Fix the security issues reported by Bandit` |
| Import errors | `@copilot Fix the import and module errors in my package` |
| Test failures | `@copilot Fix the failing tests in [file name]` |
| All analyze issues | `@copilot Fix all the issues from the failed Analyze check` |

## Getting Help

If Copilot cannot fix your CI issue:

1. **Ask for guidance**:
```
@copilot I'm stuck on this CI failure. Can you explain what's wrong and suggest how to fix it manually?
```

2. **Request team help**:
```
@azure/azure-sdk [Copilot wasn't able to fix this CI issue. Can someone help?]
```

3. **Check documentation**:
   - [CONTRIBUTING.md](https://github.com/Azure/azure-sdk-for-python/blob/main/CONTRIBUTING.md)
   - [Engineering System Checks](https://github.com/Azure/azure-sdk-for-python/blob/main/doc/eng_sys_checks.md)

## Additional Resources

- **Azure SDK Python Guidelines**: https://azure.github.io/azure-sdk/python_introduction.html
- **GitHub Copilot Documentation**: https://docs.github.com/en/copilot
- **Test Proxy Documentation**: https://github.com/Azure/azure-sdk-tools/tree/main/tools/test-proxy

---

**Remember**: GitHub Copilot's coding agent is here to help you fix CI issues quickly and learn best practices. Don't hesitate to ask for help, explanations, or alternative approaches!