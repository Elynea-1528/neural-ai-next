# Integration Test for Bootstrap Core

## Overview

This document describes the integration test suite for the `bootstrap_core` function and related components in the Neural AI Next system.

## Test File Location

- **Source**: [`tests/integration/test_bootstrap.py`](../../../tests/integration/test_bootstrap.py)

## Test Structure

The test suite is organized into three main test classes:

### 1. TestBootstrapCoreIntegration

Integration tests for the `bootstrap_core` function, testing the complete initialization flow of core components.

**Test Methods:**

- `test_bootstrap_core_returns_core_components()`: Verifies that `bootstrap_core` returns a `CoreComponents` instance
- `test_bootstrap_core_initializes_all_components()`: Ensures all core components are properly initialized
- `test_bootstrap_core_with_custom_config_path()`: Tests bootstrap with custom configuration path
- `test_bootstrap_core_with_custom_log_level()`: Tests bootstrap with custom log level
- `test_bootstrap_core_registers_components_in_container()`: Verifies DI container registration
- `test_bootstrap_core_validation_passes()`: Tests component validation
- `test_bootstrap_core_handles_missing_config_file()`: Tests error handling for missing config files
- `test_bootstrap_core_with_async_database_initialization()`: Tests async database initialization
- `test_bootstrap_core_with_async_event_bus()`: Tests async event bus startup

### 2. TestGetCoreComponentsIntegration

Integration tests for the `get_core_components` singleton function.

**Test Methods:**

- `test_get_core_components_returns_singleton()`: Verifies singleton pattern implementation
- `test_get_core_components_returns_core_components()`: Ensures correct return type

### 3. TestCoreComponentsIntegration

Integration tests for the `CoreComponents` class methods and properties.

**Test Methods:**

- `test_core_components_has_all_required_properties()`: Tests all component properties exist
- `test_core_components_has_methods_work_correctly()`: Tests `has_*` methods
- `test_core_components_set_methods_work_correctly()`: Tests `set_*` methods for testing purposes

## Test Coverage

The test suite provides comprehensive coverage of:

1. **Component Initialization**: All six core components (config, logger, storage, database, event_bus, hardware)
2. **Dependency Injection**: DI container registration and resolution
3. **Configuration**: Custom config paths and log levels
4. **Async Operations**: Database initialization and event bus startup
5. **Error Handling**: Missing configuration files
6. **Singleton Pattern**: Global component access
7. **Validation**: Component presence and integrity checks

## Testing Approach

### Mocking Strategy

The tests use extensive mocking to isolate the bootstrap process:

- **Factory Methods**: All factory methods are mocked to prevent actual component initialization
- **Async Methods**: AsyncMock is used for async methods like `initialize()` and `start()`
- **Interface Compliance**: Mock objects implement the correct interfaces using `spec` parameter

### Test Isolation

Each test is completely isolated:

- Fresh mocks for each test method
- No shared state between tests
- Independent verification of each component

### Integration Focus

While using mocks, the tests focus on integration aspects:

- Component interaction through the DI container
- Proper initialization order
- Interface contracts between components
- Error propagation

## Running the Tests

### Run All Tests

```bash
pytest tests/integration/test_bootstrap.py -v
```

### Run Specific Test Class

```bash
pytest tests/integration/test_bootstrap.py::TestBootstrapCoreIntegration -v
```

### Run with Coverage

```bash
pytest tests/integration/test_bootstrap.py --cov=neural_ai.core --cov-report=html
```

## Test Results

### Expected Results

- **All tests should pass** (14 tests)
- **No errors** in component initialization
- **Proper DI container registration** for all components
- **Correct singleton behavior** for `get_core_components`

### Common Warnings

The tests may produce warnings related to:

- **Singleton pattern verification**: Mock objects don't implement singleton pattern
- **Pydantic deprecation**: `json_encoders` deprecation warnings

These warnings are expected and do not indicate test failures.

## Test Dependencies

The test suite depends on:

- `pytest`: Test framework
- `pytest-asyncio`: Async test support
- `unittest.mock`: Mocking framework
- Core components from `neural_ai.core`

## Maintenance

### Adding New Tests

When adding new tests:

1. Follow the existing test structure
2. Use proper mocking for all external dependencies
3. Add comprehensive docstrings
4. Ensure tests are isolated and independent
5. Follow the naming convention: `test_<method>_<scenario>_<expected_result>`

### Updating Tests

When updating tests:

1. Update mock objects when interfaces change
2. Verify all component interactions are still valid
3. Ensure error handling tests cover new error scenarios
4. Update documentation to reflect changes

## Related Documentation

- [`neural_ai/core/__init__.py`](../neural_ai/core/__init__.md): Bootstrap implementation
- [`neural_ai/core/base/implementations/component_bundle.md`](../neural_ai/core/base/implementations/component_bundle.md): CoreComponents class
- [Architecture Standards](../../development/architecture_standards.md): System architecture guidelines