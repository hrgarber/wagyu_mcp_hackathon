# Mac Zsh Setup Guide

## Prerequisites Check & Installation

1. Check if Homebrew is installed:
```bash
which brew
```
If not installed:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2. Check if Git is installed:
```bash
git --version
```
If not installed:
```bash
brew install git
```

## Oh My Zsh Setup

1. Check if Oh My Zsh is installed:
```bash
ls ~/.oh-my-zsh
```
If not installed:
```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

## Configuration

1. Check your current shell:
```bash
echo $SHELL
```
If not zsh:
```bash
chsh -s $(which zsh)
```

2. Edit your ~/.zshrc:
```bash
# Theme
ZSH_THEME="clean"

# Plugin
plugins=(git)

# Colors
export TERM="xterm-256color"
```

3. Apply changes:
```bash
source ~/.zshrc
```

## Maintenance

- Update Oh My Zsh when needed:
```bash
omz update