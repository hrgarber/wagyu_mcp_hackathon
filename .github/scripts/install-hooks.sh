#!/bin/bash
# Script to install git hooks for the project
# This makes it easy for new developers to set up the hooks

# Exit on error
set -e

# Get the root directory of the git repository
REPO_ROOT=$(git rev-parse --show-toplevel)
HOOKS_DIR="$REPO_ROOT/.git/hooks"
SOURCE_DIR="$REPO_ROOT/.github/hooks"

echo "Installing git hooks..."

# Make sure all hook scripts are executable
find "$SOURCE_DIR" -type f -name "*.sh" -exec chmod +x {} \;
chmod +x "$SOURCE_DIR/pre-commit"

# Create symlinks for each hook
ln -sf "$SOURCE_DIR/pre-commit" "$HOOKS_DIR/pre-commit"

echo "Hooks installed successfully!"
echo "The following hooks are now active:"
echo "- pre-commit: Prevents committing sensitive information like API keys"
echo ""
echo "To bypass hooks in emergency situations, use: git commit --no-verify"
