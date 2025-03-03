# Wagyu Sports MCP Tests

This directory contains tests for the Wagyu Sports MCP server implementation.

## Test Files

- `test_odds_api.py` - Tests for the core Odds API client
- `test_odds_mcp_server.py` - Tests for the MCP server implementation
- `test_simple_mcp.py` - Simple direct tests for the MCP server functionality

## How to Run the Tests

The project uses pytest for running tests. The configuration is in `wagyu_sports/config/pytest.ini`.

### Using pytest directly

```bash
# Run all tests from the wagyu_sports directory
cd wagyu_sports
pytest

# Run specific test file
pytest tests/test_odds_mcp_server.py

# Run with verbose output (already default in pytest.ini)
pytest tests/test_odds_mcp_server.py

# Run a specific test function
pytest tests/test_odds_mcp_server.py::test_get_sports
```

### Environment Setup

The tests use the `test_mode=True` flag to run with mock data instead of making real API calls. This is handled automatically in the test code.

### Pytest Configuration

The project's pytest.ini configuration:
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_functions = test_*
addopts = -v
```

This configuration automatically:
- Looks for tests in the `tests` directory
- Runs files that start with `test_`
- Runs functions that start with `test_`
- Uses verbose output by default

## How to Add New Tests

### Test Approaches

There are two main approaches to testing the MCP server:

1. **Client-based testing** (in `test_odds_mcp_server.py`):
   - Uses the MCP client session to test the server through the MCP protocol
   - Tests the full protocol implementation
   - Good for integration testing

2. **Direct testing** (in `test_simple_mcp.py`):
   - Tests the server methods directly
   - Faster and simpler for testing core functionality
   - Good for unit testing

### Client-Based Test Structure

Client-based tests for the MCP server should follow this pattern:

```python
@pytest.mark.anyio
async def test_your_feature():
    """Test description"""
    # Initialize server in test mode
    server = OddsMcpServer(test_mode=True)
    
    # Create client session
    async with client_session(server.server) as client:
        # Call the tool
        result = await client.call_tool("tool_name", {"param": "value"})
        
        # Assert results
        assert len(result.content) > 0
        content = result.content[0]
        assert isinstance(content, TextContent)
        
        # Add specific assertions for your test case
        assert "expected_value" in content.text
```

### Direct Test Structure

Direct tests access the server methods directly:

```python
@pytest.mark.asyncio
async def test_direct_method():
    """Test description"""
    # Initialize server in test mode
    server = OddsMcpServer(test_mode=True)
    
    # Test method directly
    mock_data = await server._get_mock_data("data_file.json")
    
    # Parse and verify the response
    data = json.loads(mock_data)
    assert "expected_key" in data
    # Add more assertions...
```

### Testing New Tools

When adding a new tool to the MCP server:

1. Add the tool implementation to `odds_client_server.py`
2. Create a mock data file in `wagyu_sports/mcp_server/mocks_live/` if needed
3. Add a test function in `test_odds_mcp_server.py` following the pattern above
4. Ensure your test verifies both the structure and content of the response

### Testing with Different Parameters

To test a tool with different parameters:

```python
@pytest.mark.anyio
async def test_tool_with_params():
    server = OddsMcpServer(test_mode=True)
    
    async with client_session(server.server) as client:
        result = await client.call_tool(
            "tool_name", 
            {
                "param1": "value1",
                "param2": "value2"
            }
        )
        # Assertions...
```

### Testing Resources

To test MCP resources:

```python
@pytest.mark.anyio
async def test_resource():
    server = OddsMcpServer(test_mode=True)
    
    async with client_session(server.server) as client:
        # List resources
        resources = await client.list_resources()
        
        # Read a resource
        result = await client.read_resource("resource://uri")
        
        # Assertions...
```
