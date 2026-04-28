# Testing Guide for SEO Content Tool

## Quick Start

### Install Testing Dependencies
```bash
pip install -r requirements.txt
```

### Run All Tests
```bash
python run_tests.py
```

## Testing Options

### Run Specific Test Categories

**Unit Tests Only** (Test individual components)
```bash
python run_tests.py --unit
```

**Route Tests Only** (Test API endpoints)
```bash
python run_tests.py --routes
```

**Integration Tests Only** (Test complete workflows)
```bash
python run_tests.py --integration
```

### Generate Coverage Report
```bash
python run_tests.py --coverage
```
This creates an HTML coverage report in `htmlcov/index.html`

### Run Specific Test File
```bash
python run_tests.py --file tests/test_config.py
```

## Test Structure

```
tests/
├── __init__.py              # Package initialization
├── conftest.py              # Pytest fixtures and configuration
├── test_config.py           # Configuration tests
├── test_models.py           # Data model tests
├── test_routes.py           # API endpoint tests
├── test_services.py         # Service layer tests
└── test_integration.py      # End-to-end workflow tests
```

## Test Coverage

- **Configuration Management** (test_config.py)
  - Environment variable handling
  - Settings initialization and validation
  - WordPress authentication

- **Data Models** (test_models.py)
  - Request/Response model validation
  - Required field validation
  - Data type checking

- **API Routes** (test_routes.py)
  - Endpoint availability
  - Request/response handling
  - Error handling
  - Status code validation

- **Services** (test_services.py)
  - OpenAI service integration
  - Prompt generation
  - Response parsing

- **Integration Tests** (test_integration.py)
  - Complete workflows (topics → outline → content)
  - CORS configuration
  - API documentation
  - Error scenarios

## Running Tests with Pytest Directly

### Run all tests with verbose output
```bash
pytest tests/ -v
```

### Run tests matching a pattern
```bash
pytest tests/ -k "test_topics" -v
```

### Run tests with specific markers
```bash
pytest tests/ -m unit -v
pytest tests/ -m integration -v
```

### Run with detailed output and full tracebacks
```bash
pytest tests/ -vv --tb=long
```

### Stop on first failure
```bash
pytest tests/ -x
```

### Show print statements
```bash
pytest tests/ -s
```

## Continuous Integration Setup

### Using GitHub Actions
Create `.github/workflows/tests.yml`:
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - run: pytest tests/ --cov=app --cov-report=xml
```

## Mocking External Services

All tests mock external services (OpenAI API, WordPress) to ensure:
- Tests run without external dependencies
- Tests are fast and reliable
- No API costs during testing
- Consistent test results

Example:
```python
@patch('app.services.openai_service.openai_service.generate_topics')
def test_endpoint(mock_generate):
    mock_generate.return_value = ["Topic 1", "Topic 2"]
    # Test your endpoint
```

## Environment Configuration for Tests

Tests automatically use `.env.example` if `.env` doesn't exist.

Required for testing:
```env
OPENAI_API_KEY=test-key-sk-1234567890abcdef
OPENAI_MODEL=gpt-4-turbo
WORDPRESS_URL=https://example.com
WORDPRESS_USERNAME=testuser
WORDPRESS_APP_PASSWORD=test-password
```

## Troubleshooting

### Tests not found
```bash
pytest --collect-only  # List all discovered tests
```

### Import errors
```bash
python -m pytest tests/  # Run pytest as module
```

### Async test issues
Ensure `conftest.py` has proper asyncio configuration

### Coverage not generated
```bash
pip install pytest-cov
pytest --cov=app --cov-report=html
```

## Best Practices

1. **Run tests before committing**
   ```bash
   python run_tests.py
   ```

2. **Check coverage regularly**
   ```bash
   python run_tests.py --coverage
   ```

3. **Test new features immediately**
   ```bash
   pytest tests/test_new_feature.py -v
   ```

4. **Use descriptive test names**
   ```python
   def test_generate_topics_with_valid_input()
   def test_generate_topics_missing_keyword()
   ```

5. **Test both success and failure cases**
   ```python
   def test_success_case()
   def test_error_handling()
   def test_validation_error()
   ```

## Performance Testing

For slow tests, use markers:
```bash
pytest tests/ -m "not slow" -v  # Skip slow tests
```

## Coverage Goals

Current coverage targets:
- Overall: 70%+
- Critical paths: 90%+
- Services: 85%+

Monitor coverage with:
```bash
python run_tests.py --coverage
```

## Next Steps

1. **Set up pre-commit hooks** to run tests automatically
2. **Configure CI/CD** to run tests on every push
3. **Add performance benchmarks** for critical operations
4. **Expand test scenarios** based on user feedback
