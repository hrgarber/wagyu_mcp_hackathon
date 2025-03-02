#!/bin/bash
# Auto-setup script for git hooks in local development
# This script is automatically triggered by GitHub Actions in CI/CD
# but can also be run manually for local development

# Exit on error
set -e

# Get the root directory of the git repository
REPO_ROOT=$(git rev-parse --show-toplevel)
cd "$REPO_ROOT"

echo "🔒 Setting up automatic git hooks..."

# Configure git to use hooks from .github/hooks
git config --local core.hooksPath .github/hooks
echo "✓ Configured git to use hooks from .github/hooks"

# Make sure all hook scripts are executable
chmod +x .github/hooks/pre-commit
echo "✓ Made pre-commit hook executable"

# Make all module scripts executable
MODULE_COUNT=0
for module in .github/hooks/modules/*.sh; do
  if [ -f "$module" ]; then
    chmod +x "$module"
    echo "✓ Made $(basename "$module") executable"
    MODULE_COUNT=$((MODULE_COUNT+1))
  fi
done

echo ""
echo "✅ Git hooks configured automatically!"
echo "The following hooks are now active:"
echo "- pre-commit: Prevents committing sensitive information like API keys"
echo ""
echo "Modules configured ($MODULE_COUNT total):"
echo "- env-check.sh: Prevents committing .env files"
echo "- api-key-check.sh: Scans for API key patterns in code"
echo ""
echo "Your repository is now protected against accidental API key commits!"
echo "This configuration will persist across all branches."
