# Testing Framework Setup for Embergard Card Bot

## File Structure

```
tests/
├── conftest.py                 # Pytest fixtures and test data
└── test_card_library.py        # Pytest-style tests
```

## Key Files

### `conftest.py`
- Contains pytest fixtures: `sample_cards_data`, `sample_warbands_data`, `temp_csv_files`, `library_with_data`
- Provides automatic setup/teardown for test data
- Uses proper pytest fixture decorators

### `test_card_library.py` 
- Uses pytest-style test classes and functions
- Takes fixtures as parameters (dependency injection)
- Clean, focused test methods

### `pyproject.toml`
- Configured for pytest with coverage reporting
- Defines test discovery patterns
- Sets up test markers and coverage exclusions

## Usage

### Install Dependencies
```bash
# Install all dependencies including test requirements
make install
pip install -r requirements-test.txt
```

### Run Tests
```bash
# Run with pytest (recommended)
make test

# Run with coverage
make test-coverage
```

### Test Commands
```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_card_library.py

# Run with verbose output
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

## Test Features

### Fixtures Available
- `sample_cards_data`: Sample DataFrame with card data
- `sample_warbands_data`: Sample DataFrame with warband data  
- `temp_csv_files`: Temporary CSV files with automatic cleanup
- `library_with_data`: Fully loaded Library instance ready for testing

### Test Categories
- **Unit tests**: Core Library class functionality
- **Integration tests**: Real data structure compatibility
- **Edge cases**: Empty queries, typos, normalization
- **Performance**: Lazy loading, deduplication

## Benefits of pytest

1. **Fixtures**: Automatic setup/teardown with dependency injection
2. **Parameterization**: Easy to test multiple inputs
3. **Better output**: Clear test failure reporting
4. **Extensibility**: Rich plugin ecosystem
5. **Coverage**: Built-in coverage integration

## Future Enhancements

Consider adding:
- Parameterized tests for multiple search scenarios
- Mock tests for Discord API interactions  
- Performance benchmarks for large datasets
- Property-based testing with Hypothesis