#!/bin/bash
# Setup script for configuring git hooks
# Run this script once after cloning the repository

# Exit on error
set -e

# Get the root directory of the git repository
REPO_ROOT=$(git rev-parse --show-toplevel)
cd "$REPO_ROOT"

echo "Setting up git hooks..."

# Configure git to use hooks from .github/hooks
git config --local core.hooksPath .github/hooks

# Make sure all hook scripts are executable
chmod +x .github/hooks/pre-commit
find .github/hooks/modules -type f -name "*.sh" -exec chmod +x {} \;

echo "Git hooks configured successfully!"
echo "The following hooks are now active:"
echo "- pre-commit: Prevents committing sensitive information like API keys"
