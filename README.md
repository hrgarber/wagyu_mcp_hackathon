# Git Security Hooks

This repository includes git hooks to prevent accidentally committing API keys and sensitive files.

## Fully Automated Setup

The hooks are automatically configured by GitHub Actions. No manual setup required!

For local development, you can run:

```bash
.github/scripts/auto-setup.sh
```

## What This Does

- Prevents committing `.env` files
- Blocks commits containing API keys
- Works automatically across all branches
- Configured automatically by CI/CD

## How It Works

We use GitHub Actions to automatically configure git hooks for all developers. The hooks are stored in `.github/hooks` and automatically set up when you push or pull.

[More details in `.github/README.md`]
