# Plan for Making Python Odds API Properly Pip-Installable

After analyzing the current state of the Python Odds API package, I've identified several issues that prevent it from being properly installed and imported. Here's a comprehensive plan to fix these issues:

## 1. Diagnose Current Issues

Currently, the package can be installed with `pip install -e .` but fails with an import error when running `run_test.py`. The main issues appear to be:

- Package structure is not following modern Python packaging best practices
- The installation process is working but the import path is not resolving correctly
- The setup.py file needs modernization
- There's a deprecation warning about legacy editable installs

## 2. Package Restructuring

### 2.1. Create a Modern Package Structure

```
api_test/wagyu_sports/
├── pyproject.toml         # New file for modern Python packaging
├── setup.py               # Updated version
├── README.md             # Existing file
├── requirements.txt      # Existing file
├── wagyu_sports/      # Package directory (new or renamed)
│   ├── __init__.py       # Updated to expose the correct modules
│   ├── odds_client.py    # Main module
│   └── utils.py          # Utilities module
└── tests/               # Separate test directory (new)
    ├── __init__.py
    ├── run_test.py       # Moved from root
    └── test_odds_client.py # Existing test
```

## 3. Update Package Files

### 3.1. Create a Modern pyproject.toml

Create a new `pyproject.toml` file to use modern Python packaging tools (PEP 517/518) with:
- Build system specification
- Project metadata
- Dependencies
- Development dependencies

### 3.2. Update setup.py

Modernize the existing setup.py:
- Ensure package discovery works correctly
- Update metadata
- Fix URL and author information
- Make sure dependencies match requirements.txt

### 3.3. Update __init__.py

Ensure the package's `__init__.py` correctly exposes the intended classes and functions.

## 4. Fix Import Paths

### 4.1. Update Import Statements

Ensure all import statements in the package are consistent with the new structure.

### 4.2. Update Test Scripts

Modify test scripts to use the correct import paths.

## 5. Testing Plan

### 5.1. Test Installation

Test the package installation in different scenarios:
- Regular install: `pip install .`
- Editable install: `pip install -e .`
- Install from source distribution: `pip install dist/*.tar.gz`

### 5.2. Test Imports

Verify imports work correctly:
- In different Python environments
- From different directories
- With different import statements

### 5.3. Functional Testing

Run the test scripts to ensure the client functions correctly:
- Basic API functionality
- Error handling
- Edge cases

## 6. Documentation Updates

### 6.1. Update README

Update installation and usage instructions in the README.md file.

### 6.2. Add Examples

Provide clear examples of how to install and use the package.

## 7. Cleanup

Remove any temporary files or old structures that are no longer needed.

## Implementation Timeline

1. Package restructuring (30 minutes)
2. Update configuration files (20 minutes)
3. Fix import paths (15 minutes)
4. Testing (20 minutes)
5. Documentation updates (15 minutes)

## Next Steps

1. Create the new directory structure
2. Create pyproject.toml
3. Update setup.py with modern configuration
4. Move and update test files
5. Test the installation process