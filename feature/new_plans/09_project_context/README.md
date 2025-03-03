# Project Context

## Overview

This document provides essential context about the Wagyu Sports project, the requirements for the enhancement, and the decisions made during the planning process.

## Project Background

Wagyu Sports is a Python client for sports betting data that interfaces with The Odds API. The client provides methods for fetching sports data, odds, and scores from various bookmakers around the world.

### Current Features

- Access to sports betting data endpoints
- Track API usage through response headers
- Support for all API parameters and options

### Current Structure

```
wagyu_sports/
├── __init__.py
├── odds_client.py        # Main client class
├── utils.py              # Utility functions
├── build/                # Build-related files
├── config/               # Configuration files
├── docs/                 # Documentation
├── examples/             # Example scripts
└── tests/                # Test files
```

## Enhancement Requirements

The primary requirements for the enhancement are:

1. **API Credit Efficiency**: Optimize API usage to minimize credit consumption
2. **Response Archiving**: Implement a permanent archive of API responses for testing and mocking
3. **Modular Design**: Restructure the codebase for better maintainability
4. **Enhanced Functionality**: Add new methods for more granular control
5. **Backward Compatibility**: Maintain compatibility with existing code

## API Documentation Summary

The Odds API has a credit-based usage system, where different endpoints and parameters consume different amounts of credits:

- `/sports` endpoint: Free (0 credits)
- `/odds` endpoint: 1 credit per region per market
- `/scores` endpoint: 1-2 credits depending on parameters
- `/events` endpoint: Free (0 credits)
- `/historical/odds` endpoint: 10 credits per region per market

The API provides response headers that track credit usage:

- `x-requests-remaining`: The usage credits remaining until the quota resets
- `x-requests-used`: The usage credits used since the last quota reset
- `x-requests-last`: The usage cost of the last API call

## Key Decisions

### 1. Response Archive vs. Traditional Cache

We chose to implement a permanent response archive rather than a traditional time-based cache because:

- The primary goal is to create a "golden dataset" for testing and mocking
- Responses should never expire
- The archive should be organized in a way that's easy to use for testing
- The archive should be human-readable

### 2. Directory Structure

We chose to create separate directories for different components because:

- It improves code organization
- It makes it easier to find specific functionality
- It follows Python best practices
- It prepares the codebase for future expansion

### 3. Granular API Methods

We chose to add granular API methods because:

- They provide more precise control over API usage
- They make it easier to optimize credit consumption
- They provide clearer documentation of credit costs
- They simplify common use cases

### 4. Parameter Validation

We chose to add parameter validation because:

- It prevents errors and wasted API credits
- It provides clearer error messages
- It improves the developer experience
- It follows best practices for API clients

## Future MCP Integration

The enhancements are designed to prepare the module for future MCP (Model Context Protocol) integration. MCP is a protocol that allows AI models to interact with external tools and data sources.

The enhancements that will facilitate MCP integration include:

1. **Modular Design**: The new directory structure and code organization will make it easier to add MCP-specific functionality
2. **Response Archive**: The archive will provide a reliable dataset for testing MCP integration
3. **Granular API Methods**: These methods will map well to MCP tools
4. **Credit Tracking**: This will help manage API usage in an MCP context

## Development Environment

- Python 3.10 or higher
- No external dependencies required for core functionality
- Testing with pytest

## Additional Resources

- [The Odds API Documentation](https://the-odds-api.com/liveapi/guides/v4/)
- [Python Type Hints Documentation](https://docs.python.org/3/library/typing.html)
- [Model Context Protocol](https://modelcontextprotocol.io/)
