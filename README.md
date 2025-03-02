# Git Security Hooks

This repository includes git hooks to prevent accidentally committing API keys and sensitive files.

## First-Time Setup

Run this once after cloning:

```bash
chmod +x .github/scripts/setup.sh
.github/scripts/setup.sh
```

## What This Does

- Prevents committing `.env` files
- Blocks commits containing API keys
- Works automatically after setup

## For Existing Developers

After pulling updates, no additional steps needed. The hooks work automatically.

## How It Works

We use Git's `core.hooksPath` to make hooks part of the repository itself, so they're automatically shared with all developers.

[More details in `.github/README.md`]
