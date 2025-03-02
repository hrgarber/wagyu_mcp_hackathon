#!/bin/bash
# Module to check for API keys in commits
# Scans for common API key patterns to prevent accidental exposure

# Define patterns to check for
# Add more patterns as needed for different types of API keys
PATTERNS=(
  # The Odds API key pattern (alphanumeric, typically 32 chars)
  "ODDS_API_KEY=[a-zA-Z0-9]{32}"
  
  # Generic API key patterns
  "api[_-]key[=\"':= ][a-zA-Z0-9]"
  "apikey[=\"':= ][a-zA-Z0-9]"
  "key[=\"':= ][a-zA-Z0-9]{32}"
  "secret[=\"':= ][a-zA-Z0-9]"
  "password[=\"':= ][a-zA-Z0-9]"
  "token[=\"':= ][a-zA-Z0-9]"
)

# Check staged files for API key patterns
for pattern in "${PATTERNS[@]}"; do
  # Use git grep to search staged changes
  matches=$(git diff --cached -U0 | grep -i -E "$pattern" || true)
  
  if [ -n "$matches" ]; then
    echo "ERROR: Potential API key or sensitive data found in commit."
    echo "Pattern matched: $pattern"
    echo ""
    echo "Please remove the sensitive data and try again."
    echo "Consider using environment variables or a secure vault."
    exit 1
  fi
done

exit 0
