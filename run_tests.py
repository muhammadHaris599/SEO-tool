"""
Comprehensive test runner for SEO Content Tool.
Runs all tests and generates coverage reports.
"""

import subprocess
import sys
from pathlib import Path


class Colors:
    """ANSI color codes for terminal output."""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'


def print_header(text):
    """Print section header."""
    print(f"\n{Colors.BLUE}{'=' * 70}")
    print(f"{text.center(70)}")
    print('=' * 70 + Colors.END)


def print_success(text):
    """Print success message."""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")


def print_error(text):
    """Print error message."""
    print(f"{Colors.RED}✗ {text}{Colors.END}")


def print_warning(text):
    """Print warning message."""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")


def print_info(text):
    """Print info message."""
    print(f"ℹ {text}")


def check_dependencies():
    """Check if testing dependencies are installed."""
    print_header("Dependency Check")
    
    required_packages = [
        "pytest",
        "pytest_asyncio",
        "pytest_cov",
        "pytest_mock",
        "fastapi"
    ]
    
    missing = []
    
    for package in required_packages:
        try:
            __import__(package.replace("_", "-"))
            print_success(f"{package} is installed")
        except ImportError:
            print_error(f"{package} is NOT installed")
            missing.append(package)
    
    if missing:
        print_warning("Some packages are missing!")
        print_info(f"Run: pip install {' '.join(missing)}")
        return False
    
    print_success("All required packages are installed")
    return True


def run_unit_tests():
    """Run unit tests."""
    print_header("Running Unit Tests")
    
    try:
        result = subprocess.run(
            [
                sys.executable, "-m", "pytest",
                "tests/test_config.py",
                "tests/test_models.py",
                "tests/test_services.py",
                "-v",
                "--tb=short"
            ],
            check=False,
            capture_output=False
        )
        
        if result.returncode == 0:
            print_success("Unit tests passed")
            return True
        else:
            print_error("Unit tests failed")
            return False
    
    except Exception as e:
        print_error(f"Error running unit tests: {str(e)}")
        return False


def run_route_tests():
    """Run route/API tests."""
    print_header("Running Route Tests")
    
    try:
        result = subprocess.run(
            [
                sys.executable, "-m", "pytest",
                "tests/test_routes.py",
                "-v",
                "--tb=short"
            ],
            check=False,
            capture_output=False
        )
        
        if result.returncode == 0:
            print_success("Route tests passed")
            return True
        else:
            print_warning("Route tests had failures")
            return False
    
    except Exception as e:
        print_error(f"Error running route tests: {str(e)}")
        return False


def run_integration_tests():
    """Run integration tests."""
    print_header("Running Integration Tests")
    
    try:
        result = subprocess.run(
            [
                sys.executable, "-m", "pytest",
                "tests/test_integration.py",
                "-v",
                "--tb=short"
            ],
            check=False,
            capture_output=False
        )
        
        if result.returncode == 0:
            print_success("Integration tests passed")
            return True
        else:
            print_warning("Integration tests had failures")
            return False
    
    except Exception as e:
        print_error(f"Error running integration tests: {str(e)}")
        return False


def run_all_tests_with_coverage():
    """Run all tests with coverage report."""
    print_header("Running All Tests with Coverage")
    
    try:
        result = subprocess.run(
            [
                sys.executable, "-m", "pytest",
                "tests/",
                "-v",
                "--cov=app",
                "--cov-report=html",
                "--cov-report=term-missing",
                "--tb=short"
            ],
            check=False,
            capture_output=False
        )
        
        if result.returncode == 0:
            print_success("All tests passed with coverage")
            print_info("Coverage report generated in htmlcov/index.html")
            return True
        else:
            print_warning("Some tests failed - check coverage report")
            return False
    
    except Exception as e:
        print_error(f"Error running tests with coverage: {str(e)}")
        return False


def run_specific_test(test_file):
    """Run a specific test file."""
    print_header(f"Running {test_file}")
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", test_file, "-v", "--tb=short"],
            check=False,
            capture_output=False
        )
        
        return result.returncode == 0
    
    except Exception as e:
        print_error(f"Error running test: {str(e)}")
        return False


def main():
    """Main test runner."""
    print_header("SEO Content Tool - Comprehensive Test Suite")
    
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Run tests for SEO Content Tool"
    )
    parser.add_argument(
        "--unit",
        action="store_true",
        help="Run only unit tests"
    )
    parser.add_argument(
        "--routes",
        action="store_true",
        help="Run only route tests"
    )
    parser.add_argument(
        "--integration",
        action="store_true",
        help="Run only integration tests"
    )
    parser.add_argument(
        "--coverage",
        action="store_true",
        help="Run all tests with coverage report"
    )
    parser.add_argument(
        "--file",
        type=str,
        help="Run a specific test file"
    )
    parser.add_argument(
        "--check-deps",
        action="store_true",
        help="Check dependencies only"
    )
    
    args = parser.parse_args()
    
    # Check dependencies first
    if not check_dependencies():
        print_error("Please install missing dependencies")
        return 1
    
    if args.check_deps:
        return 0
    
    if args.file:
        success = run_specific_test(args.file)
        return 0 if success else 1
    
    if args.unit:
        success = run_unit_tests()
        return 0 if success else 1
    
    if args.routes:
        success = run_route_tests()
        return 0 if success else 1
    
    if args.integration:
        success = run_integration_tests()
        return 0 if success else 1
    
    if args.coverage:
        success = run_all_tests_with_coverage()
        return 0 if success else 1
    
    # Default: run all tests
    print_header("Running Complete Test Suite")
    
    results = {
        "Dependencies": True,  # Already checked
        "Unit Tests": run_unit_tests(),
        "Route Tests": run_route_tests(),
        "Integration Tests": run_integration_tests(),
    }
    
    print_header("Test Summary")
    
    all_passed = True
    for test_type, result in results.items():
        if result:
            print_success(f"{test_type}: PASSED")
        else:
            print_error(f"{test_type}: FAILED")
            all_passed = False
    
    print_info("\nRun 'python run_tests.py --coverage' for detailed coverage report")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
