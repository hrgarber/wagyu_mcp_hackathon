# Python Odds API Fix Task Context

## Current State

- Branch: `fix/python_api`
- Working Directory: `/Users/brandonbutterwick/Documents/hackathon/wagyu_mcp_hackathon`
- Project Location: `api_test/python_odds_api/`

## Background Context

1. The Python Odds API package is currently experiencing installation and import issues
2. A friend's PC was able to run the package successfully, indicating environment-specific problems
3. The package uses a conda environment named 'sports' for development
4. Current dependencies are managed through requirements.txt:
   - requests>=2.25.0
   - python-dotenv>=0.15.0

## Known Issues

1. Package fails to import when running `run_test.py`
2. Legacy editable install warning appears during pip installation
3. Import paths are not resolving correctly
4. Package structure needs modernization

## Environment Setup

1. Conda environment 'sports' is being used
2. Dependencies have been installed in the conda environment
3. The .env file contains the ODDS_API_KEY for testing

## Recent Changes

1. Created detailed implementation plan in `docs/pip_install_fix_plan.md`
2. No structural changes have been made yet
3. Original package structure and files remain intact

## Next Action Items

1. Create new directory structure as outlined in the plan
2. Implement modern Python packaging with pyproject.toml
3. Update package configuration in setup.py
4. Reorganize test files into dedicated test directory

## Important Files

- `run_test.py`: Main test script showing import issues
- `odds_client.py`: Core client implementation
- `setup.py`: Package configuration (needs modernization)
- `.env`: Contains API key for testing
- `requirements.txt`: Current dependency specifications

## Testing Notes

1. Test script requires ODDS_API_KEY environment variable
2. Current test failure is at import level, not API functionality
3. Package should be tested in both regular and editable install modes

## Additional Context

1. Package is intended to be pip-installable for end users
2. Need to maintain compatibility with existing API usage patterns
3. Modern Python packaging practices should be followed
4. Documentation needs to be updated after fixes

This context document should help Roo pick up the task and continue with the implementation phase of the pip installation fixes.