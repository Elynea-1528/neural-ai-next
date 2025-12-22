"""Unit tests for scripts.install.__init__ module.

This module contains comprehensive tests for the installation system
components including InstallationError, InstallationConfig, and
InstallationController classes.
"""

import unittest
from unittest.mock import Mock, patch

from scripts.install import (
    InstallationConfig,
    InstallationController,
    InstallationError,
    installation_controller,
)


class TestInstallationError(unittest.TestCase):
    """Test cases for InstallationError class."""

    def test_installation_error_creation(self) -> None:
        """Test InstallationError creation with all parameters."""
        error = InstallationError(
            message="Test error message", error_code="TEST_ERROR", installation_step="test_step"
        )
        self.assertEqual(error.message, "Test error message")
        self.assertEqual(error.error_code, "TEST_ERROR")
        self.assertEqual(error.installation_step, "test_step")

    def test_installation_error_creation_minimal(self) -> None:
        """Test InstallationError creation with minimal parameters."""
        error = InstallationError(message="Test error message")
        self.assertEqual(error.message, "Test error message")
        self.assertIsNone(error.error_code)
        self.assertIsNone(error.installation_step)

    def test_installation_error_inheritance(self) -> None:
        """Test that InstallationError properly inherits from Exception."""
        error = InstallationError(message="Test error")
        self.assertIsInstance(error, Exception)


class TestInstallationConfig(unittest.TestCase):
    """Test cases for InstallationConfig class."""

    def test_installation_config_creation(self) -> None:
        """Test InstallationConfig creation."""
        config = InstallationConfig()
        self.assertIsInstance(config.config_data, dict)
        self.assertEqual(config.config_data, {})

    def test_installation_config_with_file_path(self) -> None:
        """Test InstallationConfig creation with file path."""
        config = InstallationConfig(config_file_path="/path/to/config.yaml")
        self.assertEqual(config.config_file_path, "/path/to/config.yaml")

    def test_default_config_returns_dict(self) -> None:
        """Test that _default_config returns a dictionary."""
        config = InstallationConfig()
        default_config = config._default_config()
        self.assertIsInstance(default_config, dict)
        self.assertIn("python_path", default_config)
        self.assertIn("dependencies", default_config)

    def test_default_config_contains_required_keys(self) -> None:
        """Test that default config contains all required keys."""
        config = InstallationConfig()
        default_config = config._default_config()
        required_keys = [
            "install_directory",
            "python_path",
            "environment_name",
            "dependencies",
            "mt5_installation",
            "wine_config",
            "jupyter_settings",
        ]
        for key in required_keys:
            self.assertIn(key, default_config)

    def test_load_config_no_file(self) -> None:
        """Test loading config when no file path is provided."""
        config = InstallationConfig()
        config.load_config()
        # Should load default config
        self.assertGreater(len(config.config_data), 0)

    def test_load_config_file_not_found(self) -> None:
        """Test loading config when file is not found.

        Note: Currently this test verifies that no exception is raised
        because the file loading is not fully implemented yet.
        """
        config = InstallationConfig(config_file_path="/nonexistent/path.yaml")
        # Should not raise an error since file loading is not implemented
        try:
            config.load_config()
        except InstallationError:
            self.fail("load_config() raised InstallationError unexpectedly")

    def test_validate_config_valid(self) -> None:
        """Test config validation with valid configuration."""
        config = InstallationConfig()
        config.load_config()
        successful, errors = config.validate_config()
        self.assertTrue(successful)
        self.assertEqual(len(errors), 0)

    def test_validate_config_invalid_python_path(self) -> None:
        """Test config validation with invalid Python path."""
        config = InstallationConfig()
        config.config_data = {"python_path": None}
        successful, errors = config.validate_config()
        self.assertFalse(successful)
        self.assertIn("Invalid Python path.", errors)

    def test_validate_config_invalid_install_directory(self) -> None:
        """Test config validation with invalid installation directory."""
        config = InstallationConfig()
        config.config_data = {"python_path": "/valid/path", "install_directory": None}
        successful, errors = config.validate_config()
        self.assertFalse(successful)
        self.assertIn("Invalid installation directory.", errors)

    def test_validate_config_invalid_dependencies(self) -> None:
        """Test config validation with invalid dependencies."""
        config = InstallationConfig()
        config.config_data = {
            "python_path": "/valid/path",
            "install_directory": "/valid/dir",
            "dependencies": None,
        }
        successful, errors = config.validate_config()
        self.assertFalse(successful)
        self.assertIn("Invalid dependency list.", errors)


class TestInstallationController(unittest.TestCase):
    """Test cases for InstallationController class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.config = InstallationConfig()
        self.logger = Mock()

    def test_installation_controller_creation(self) -> None:
        """Test InstallationController creation."""
        controller = InstallationController(config=self.config)
        self.assertIsInstance(controller.installation_steps, list)
        self.assertEqual(len(controller.installation_steps), 0)

    def test_installation_controller_with_logger(self) -> None:
        """Test InstallationController creation with logger."""
        controller = InstallationController(config=self.config, logger=self.logger)
        self.assertEqual(controller.logger, self.logger)

    def test_add_installation_step(self) -> None:
        """Test adding installation steps."""
        controller = InstallationController(config=self.config)
        controller.add_installation_step("test_step")
        self.assertIn("test_step", controller.installation_steps)

    def test_add_installation_step_duplicate(self) -> None:
        """Test adding duplicate installation steps."""
        controller = InstallationController(config=self.config)
        controller.add_installation_step("test_step")
        controller.add_installation_step("test_step")
        # Should not add duplicate
        self.assertEqual(controller.installation_steps.count("test_step"), 1)

    def test_remove_installation_step(self) -> None:
        """Test removing installation steps."""
        controller = InstallationController(config=self.config)
        controller.add_installation_step("test_step")
        controller.remove_installation_step("test_step")
        self.assertNotIn("test_step", controller.installation_steps)

    def test_remove_nonexistent_installation_step(self) -> None:
        """Test removing non-existent installation step."""
        controller = InstallationController(config=self.config)
        # Should not raise error
        controller.remove_installation_step("nonexistent_step")

    def test_set_default_steps(self) -> None:
        """Test setting default installation steps."""
        controller = InstallationController(config=self.config)
        controller._set_default_steps()
        expected_steps = [
            "check_dependencies",
            "activate_environment",
            "create_install_directory",
            "install_dependencies",
            "setup_jupyter",
        ]
        for step in expected_steps:
            self.assertIn(step, controller.installation_steps)

    def test_set_default_steps_with_mt5(self) -> None:
        """Test setting default steps including MT5 setup."""
        self.config.config_data = {"mt5_installation": True}
        controller = InstallationController(config=self.config)
        controller._set_default_steps()
        self.assertIn("setup_mt5", controller.installation_steps)

    def test_set_default_steps_without_mt5(self) -> None:
        """Test setting default steps without MT5 setup."""
        self.config.config_data = {"mt5_installation": False}
        controller = InstallationController(config=self.config)
        controller._set_default_steps()
        self.assertNotIn("setup_mt5", controller.installation_steps)

    def test_execute_step_valid(self) -> None:
        """Test executing a valid installation step."""
        controller = InstallationController(config=self.config, logger=self.logger)
        # Mock the step function
        controller._check_dependencies = Mock()  # type: ignore
        controller._execute_step("check_dependencies")
        controller._check_dependencies.assert_called_once()

    def test_execute_step_invalid(self) -> None:
        """Test executing an invalid installation step."""
        controller = InstallationController(config=self.config)
        with self.assertRaises(InstallationError) as context:
            controller._execute_step("invalid_step")
        self.assertEqual(context.exception.error_code, "UNKNOWN_STEP")

    @patch.object(InstallationConfig, "load_config")
    @patch.object(InstallationConfig, "validate_config")
    def test_start_installation_success(self, mock_validate: Mock, mock_load: Mock) -> None:
        """Test successful installation start."""
        mock_validate.return_value = (True, [])
        controller = InstallationController(config=self.config, logger=self.logger)
        # Mock the step execution
        controller._execute_step = Mock()  # type: ignore

        result = controller.start_installation()
        self.assertTrue(result)
        mock_load.assert_called_once()
        mock_validate.assert_called_once()

    @patch.object(InstallationConfig, "load_config")
    @patch.object(InstallationConfig, "validate_config")
    def test_start_installation_validation_failure(
        self, mock_validate: Mock, mock_load: Mock
    ) -> None:
        """Test installation start with validation failure."""
        mock_validate.return_value = (False, ["Test error"])
        controller = InstallationController(config=self.config, logger=self.logger)

        with self.assertRaises(InstallationError) as context:
            controller.start_installation()
        self.assertEqual(context.exception.error_code, "CONFIG_VALIDATION_ERROR")

    def test_step_methods_are_callable(self) -> None:
        """Test that all step methods are callable."""
        controller = InstallationController(config=self.config, logger=self.logger)
        step_methods = [
            "_check_dependencies",
            "_activate_environment",
            "_create_install_directory",
            "_install_dependencies",
            "_setup_mt5",
            "_setup_jupyter",
        ]
        for method_name in step_methods:
            method = getattr(controller, method_name)
            self.assertTrue(callable(method))

    def test_check_dependencies_execution(self) -> None:
        """Test that _check_dependencies method executes without error."""
        controller = InstallationController(config=self.config, logger=self.logger)
        # Should not raise any exception
        controller._check_dependencies()
        # Verify logger was called if present
        if self.logger:
            self.logger.info.assert_called()

    def test_check_dependencies_with_dependencies(self) -> None:
        """Test that _check_dependencies handles dependencies list."""
        self.config.config_data = {"dependencies": ["numpy", "pytest"]}
        controller = InstallationController(config=self.config, logger=self.logger)
        # Should not raise any exception
        controller._check_dependencies()
        # Verify logger was called if present
        if self.logger:
            self.logger.info.assert_called()

    def test_activate_environment_execution(self) -> None:
        """Test that _activate_environment method executes without error."""
        controller = InstallationController(config=self.config, logger=self.logger)
        # Should not raise any exception
        controller._activate_environment()
        # Verify logger was called if present
        if self.logger:
            self.logger.info.assert_called()

    def test_activate_environment_with_env_name(self) -> None:
        """Test that _activate_environment handles environment name."""
        self.config.config_data = {"environment_name": "test-env"}
        controller = InstallationController(config=self.config, logger=self.logger)
        # Should not raise any exception
        controller._activate_environment()
        # Verify logger was called if present
        if self.logger:
            self.logger.info.assert_called()

    def test_create_install_directory_execution(self) -> None:
        """Test that _create_install_directory method executes without error."""
        controller = InstallationController(config=self.config, logger=self.logger)
        # Should not raise any exception
        controller._create_install_directory()
        # Verify logger was called if present
        if self.logger:
            self.logger.info.assert_called()

    def test_create_install_directory_with_path(self) -> None:
        """Test that _create_install_directory handles install directory."""
        self.config.config_data = {"install_directory": "/opt/test"}
        controller = InstallationController(config=self.config, logger=self.logger)
        # Should not raise any exception
        controller._create_install_directory()
        # Verify logger was called if present
        if self.logger:
            self.logger.info.assert_called()

    def test_install_dependencies_execution(self) -> None:
        """Test that _install_dependencies method executes without error."""
        controller = InstallationController(config=self.config, logger=self.logger)
        # Should not raise any exception
        controller._install_dependencies()
        # Verify logger was called if present
        if self.logger:
            self.logger.info.assert_called()

    def test_install_dependencies_with_list(self) -> None:
        """Test that _install_dependencies handles dependencies list."""
        self.config.config_data = {"dependencies": ["numpy", "pytest"]}
        controller = InstallationController(config=self.config, logger=self.logger)
        # Should not raise any exception
        controller._install_dependencies()
        # Verify logger was called if present
        if self.logger:
            self.logger.info.assert_called()

    def test_setup_mt5_execution(self) -> None:
        """Test that _setup_mt5 method executes without error."""
        controller = InstallationController(config=self.config, logger=self.logger)
        # Should not raise any exception
        controller._setup_mt5()
        # Verify logger was called if present
        if self.logger:
            self.logger.info.assert_called()

    def test_setup_mt5_with_config(self) -> None:
        """Test that _setup_mt5 handles wine config."""
        self.config.config_data = {"wine_config": {"prefix": "~/.wine-test"}}
        controller = InstallationController(config=self.config, logger=self.logger)
        # Should not raise any exception
        controller._setup_mt5()
        # Verify logger was called if present
        if self.logger:
            self.logger.info.assert_called()

    def test_setup_jupyter_execution(self) -> None:
        """Test that _setup_jupyter method executes without error."""
        controller = InstallationController(config=self.config, logger=self.logger)
        # Should not raise any exception
        controller._setup_jupyter()
        # Verify logger was called if present
        if self.logger:
            self.logger.info.assert_called()

    def test_setup_jupyter_with_settings(self) -> None:
        """Test that _setup_jupyter handles jupyter settings."""
        self.config.config_data = {"jupyter_settings": {"port": 9999}}
        controller = InstallationController(config=self.config, logger=self.logger)
        # Should not raise any exception
        controller._setup_jupyter()
        # Verify logger was called if present
        if self.logger:
            self.logger.info.assert_called()


class TestInstallationControllerFactory(unittest.TestCase):
    """Test cases for installation_controller factory function."""

    def test_installation_controller_factory_no_params(self) -> None:
        """Test factory function with no parameters."""
        controller = installation_controller()
        self.assertIsInstance(controller, InstallationController)

    def test_installation_controller_factory_with_config(self) -> None:
        """Test factory function with config parameter."""
        config = InstallationConfig()
        controller = installation_controller(config=config)
        self.assertEqual(controller.config, config)

    def test_installation_controller_factory_with_logger(self) -> None:
        """Test factory function with logger parameter."""
        logger = Mock()
        controller = installation_controller(logger=logger)
        self.assertEqual(controller.logger, logger)

    def test_installation_controller_factory_with_all_params(self) -> None:
        """Test factory function with all parameters."""
        config = InstallationConfig()
        logger = Mock()
        controller = installation_controller(config=config, logger=logger)
        self.assertEqual(controller.config, config)
        self.assertEqual(controller.logger, logger)


if __name__ == "__main__":
    unittest.main()
