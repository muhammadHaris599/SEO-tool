# Quick Testing Guide

## Setup (One Time)

```bash
cd c:\Users\wahab.ikram\Desktop\SEOTool
python -m pip install -r requirements.txt
```

## Running Tests

### Option 1: Using the Test Runner Script
```bash
python run_tests.py
```

### Option 2: Run Specific Test Categories
```bash
# Unit tests only
python run_tests.py --unit

# API route tests only  
python run_tests.py --routes

# Integration tests only
python run_tests.py --integration

# With coverage report
python run_tests.py --coverage
```

### Option 3: Using pytest Directly
```bash
# All tests
python -m pytest tests/ -v

# Specific test file
python -m pytest tests/test_config.py -v

# With coverage
python -m pytest tests/ --cov=app --cov-report=html
```

## Test Files Created

- `tests/test_config.py` - Configuration and settings tests
- `tests/test_models.py` - Data model validation tests  
- `tests/test_routes.py` - API endpoint tests
- `tests/test_services.py` - Service layer tests
- `tests/test_integration.py` - End-to-end workflow tests

## What Each Test Category Covers

**Configuration Tests**
- Environment variable loading
- Settings validation
- WordPress credentials handling

**Model Tests** 
- Request/response validation
- Required field checking
- Type validation

**Route Tests**
- API endpoint availability
- Request handling
- Error responses
- Status codes

**Service Tests**
- OpenAI integration
- Prompt generation  
- Response parsing

**Integration Tests**
- Complete workflows (topic → outline → content)
- CORS handling
- API documentation
- Error scenarios

## Understanding Test Output

✓ = Test passed
✗ = Test failed  
⚠ = Warning/skip

Coverage report shows what % of code is tested.

## Next Steps

1. **Run tests after each change** to catch issues early
2. **Check coverage** to identify untested code
3. **Add new tests** when adding features
4. **Review failures** to understand issues

## Tips

- Use `pytest -k "test_name"` to run specific tests
- Use `pytest -x` to stop on first failure  
- Use `pytest -v` for verbose output
- Use `pytest -s` to see print statements
