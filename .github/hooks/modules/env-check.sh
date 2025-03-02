#!/bin/bash
# Module to check for .env files in commits
# Prevents accidentally committing environment files with sensitive data

# Check for .env files in the staged changes
if git diff --cached --name-only | grep -q "\.env$"; then
  echo "ERROR: Attempting to commit .env file."
  echo "These files typically contain sensitive information like API keys."
  echo "Add them to .gitignore instead and use .env.example as a template."
  echo ""
  echo "Offending files:"
  git diff --cached --name-only | grep "\.env$"
  exit 1
fi

# Also check for files that might be .env files with different extensions
if git diff --cached --name-only | grep -q "env\.\|\.env\."; then
  echo "WARNING: Possible environment file detected."
  echo "Please verify these files don't contain sensitive information:"
  git diff --cached --name-only | grep "env\.\|\.env\."
  echo ""
  echo "Continue with commit? (y/n)"
  read -r response
  if [[ "$response" != "y" ]]; then
    exit 1
  fi
fi

exit 0
