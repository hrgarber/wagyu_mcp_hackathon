# Wagyu Sports API

The Wagyu Sports API client for sports betting data, providing access to The Odds API v4 and other sports data sources.

```mermaid
graph LR
    User([Your Code]) --> Client[Wagyu Sports Client] --> API[The Odds API]
    MCP[MCP Server] --> Client
    Client --> MCP
    API --> Client --> User
    
    style User fill:#f8f8f8,stroke:#666,stroke-width:1px,color:#000
    style Client fill:#4285F4,stroke:#2965C9,stroke-width:2px,color:#fff
    style API fill:#F5F5F5,stroke:#999,stroke-width:1px,color:#000
    style MCP fill:#34A853,stroke:#1E8E3E,stroke-width:2px,color:#fff
```

## Directory Structure

The project has been reorganized for better maintainability:
- `wagyu_sports/build/` - Build-related files (pyproject.toml, requirements.txt, setup.py)
- `wagyu_sports/config/` - Configuration files (.env.example, pytest.ini)
- `wagyu_sports/docs/` - Documentation (LICENSE, README.md)
- `wagyu_sports/examples/` - Example scripts
- `wagyu_sports/mcp_server/` - Model Context Protocol (MCP) server implementation
- `wagyu_sports/tests/` - Test files

## Installation

```bash
# Development installation
uvx install -e .

# User installation
uv install wagyu_sports

# Set up API key
cp wagyu_sports/config/.env.example wagyu_sports/config/.env
# Add your API key to .env (get one from https://the-odds-api.com/)
```

## Running the MCP Server

```bash
# Run the MCP server directly
uvx run wagyu_sports.mcp_server.test_server
```

## Usage

```python
from wagyu_sports import OddsClient
import os
from dotenv import load_dotenv

# Load API key
load_dotenv(dotenv_path="wagyu_sports/config/.env")
api_key = os.getenv("ODDS_API_KEY")

# Get sports data
client = OddsClient(api_key)
sports = client.get_sports()
print(f"Available sports: {len(sports['data'])}")

# Get odds for NBA
odds = client.get_odds("basketball_nba", {"regions": "us", "markets": "h2h"})
```

## Features

- Access all endpoints of The Odds API v4
- Track API usage through response headers
- Support for all API parameters and options
- Utility functions for saving responses and testing

## Examples

The `wagyu_sports/examples/` directory contains:
- `example.py`: Basic usage
- `advanced_example.py`: Error handling, quota management, data processing
- `fetch_nba_odds.py`: NBA-specific example
- `verify_install.py`: Installation verification

## Testing

The project includes multiple test approaches:

```bash
# Install test dependencies
uvx install pytest pytest-asyncio

# Run all tests
uvx run pytest wagyu_sports/tests

# Run specific test file
uvx run pytest wagyu_sports/tests/test_simple_mcp.py
```

### Test Types

- **API Client Tests**: Tests for the core Odds API client functionality
- **MCP Server Tests**: Tests for the MCP server implementation
  - **Client-based tests**: Test the full MCP protocol implementation
  - **Direct tests**: Simpler tests that directly test server methods

## Git Hooks

This repository includes a post-commit hook that automatically deletes Python cache files:

- Automatically removes all `__pycache__` directories after each commit
- Deletes `.pyc`, `.pyo`, and `.pyd` compiled Python files
- Keeps your working directory clean while developing

The hook is already set up in `.git/hooks/post-commit`. If you clone this repository, you'll need to make the hook executable:
```bash
chmod +x .git/hooks/post-commit
```

## API Documentation

For full API documentation, visit [The Odds API](https://the-odds-api.com/liveapi/guides/v4/).
