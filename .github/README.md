# Git Security Hooks

This directory contains git hooks designed to prevent accidental commits of sensitive information like API keys and environment files.

## Features

- **Prevents committing `.env` files** that typically contain sensitive information
- **Scans for API key patterns** in staged changes
- **Modular design** that's easy to extend with additional checks

## Installation

Run the installation script to set up the hooks:

```bash
# Make the script executable
chmod +x .github/scripts/install-hooks.sh

# Run the installation script
.github/scripts/install-hooks.sh
```

## How It Works

The pre-commit hook runs a series of checks before allowing a commit:

1. **env-check.sh**: Prevents committing `.env` files
2. **api-key-check.sh**: Scans for API key patterns in staged changes

## Adding New Checks

To add a new security check:

1. Create a new script in `.github/hooks/modules/`
2. Make it executable (`chmod +x your-script.sh`)
3. The main pre-commit hook will automatically include it

## Bypassing Hooks

In emergency situations, you can bypass the hooks with:

```bash
git commit --no-verify
```

**Note**: Only do this when absolutely necessary, and make sure to clean up any sensitive information afterward.

## Future Extensions

This hook system is designed to be easily extended. Some ideas for future additions:

- Scanning for other types of secrets (SSH keys, certificates)
- Integration with secret scanning tools
- Custom checks for project-specific sensitive data
