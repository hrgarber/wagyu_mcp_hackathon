# Python Odds API Client

A Python client for The Odds API v4, providing access to sports betting data.

## Installation

```bash
# Install the package
pip install -e .

# Set up API key
cp .env.example .env
# Edit .env and add your API key from https://the-odds-api.com/
```

## Quick Start

```python
from python_odds_api import OddsClient
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
api_key = os.getenv("ODDS_API_KEY")

# Create client and get sports
client = OddsClient(api_key)
sports = client.get_sports()
print(f"Available sports: {len(sports['data'])}")
```

## Features

- Access all endpoints of The Odds API v4
- Track API usage through response headers
- Support for all API parameters and options

## Examples

See the `examples/` directory for usage patterns:
- `examples/example.py`: Basic usage
- `examples/advanced_example.py`: Advanced features
- `examples/verify_install.py`: Verify installation
- `examples/fetch_nba_odds.py`: Fetch NBA odds example
- `examples/verify_import.py`: Simple import verification

## Testing

Run the tests using pytest:

```bash
# Install pytest if not already installed
pip install pytest

# Run tests
pytest
```

Or use the Makefile:

```bash
make test
