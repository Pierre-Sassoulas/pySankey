# pySankey - Sankey Diagram Generator

pySankey is a Python package that creates beautiful Sankey diagrams using matplotlib. It generates flow diagrams that show the flow of quantities between categories from left to right.

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively

### Bootstrap, Build, and Test the Repository
- `pip install -e ".[test]"` -- takes 25-30 seconds. NEVER CANCEL. Set timeout to 60+ seconds.
- `pytest .` -- takes 3-4 seconds. NEVER CANCEL. Set timeout to 30+ seconds.
- `python -m unittest` -- alternative test runner, takes 1-2 seconds. NEVER CANCEL. Set timeout to 30+ seconds.

### Code Quality and Linting
- `pylint pysankey` -- takes 10-12 seconds. NEVER CANCEL. Set timeout to 30+ seconds.
- `ruff check .` -- extremely fast (<0.1 seconds), shows linting issues
- `ruff check --fix .` -- automatically fixes most linting issues
- `ruff format .` -- formats code, extremely fast (<0.1 seconds)

### Coverage Testing
- `coverage run -m pytest .` -- takes 3-4 seconds. NEVER CANCEL. Set timeout to 30+ seconds.
- `coverage html` -- generates HTML report in htmlcov/index.html, takes 3 seconds. NEVER CANCEL. Set timeout to 30+ seconds.

### Building Packages (Network Dependent)
- `python -m build` -- UNRELIABLE due to network timeouts in this environment. Use for documentation only.
- Pre-commit hooks (`pre-commit run --all-files`) -- UNRELIABLE due to network timeouts in this environment.

## Validation

- ALWAYS test basic functionality after making changes by running a Sankey diagram creation test.
- ALWAYS run `pytest .` or `python -m unittest` before committing changes.
- ALWAYS run `ruff check . && ruff format .` to ensure code quality.
- Test both basic fruit data example and customer-goods example to validate functionality.

### Manual Validation Scenario
After making changes, validate with this test:
```python
import pandas as pd
from pysankey import sankey
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

# Test basic functionality
df = pd.read_csv('pysankey/fruits.txt', sep=' ', names=['true', 'predicted'])
ax = sankey(
    left=df['true'],
    right=df['predicted'],
    aspect=20,
    fontsize=12
)
plt.savefig('/tmp/validation_test.png', bbox_inches='tight', dpi=150)
print("✓ Validation successful - Sankey diagram created")
```

## Critical Build Information

- **Installation time**: ~25-30 seconds for full development environment
- **Test time**: 3-4 seconds for complete test suite (10 tests)
- **Linting time**: 10-12 seconds for pylint, <0.1 seconds for ruff
- **Coverage time**: 3-4 seconds for test coverage, 3 seconds for HTML report generation
- **Python versions**: Supports 3.8, 3.9, 3.10, 3.11, 3.12

## Repository Structure

### Key Directories
- `pysankey/` - Main source code
  - `__init__.py` - Package initialization and exports
  - `sankey/` - Core Sankey diagram implementation
  - `fruits.txt` - Sample fruit classification data (1041 rows)
  - `customers-goods.csv` - Sample customer-goods transaction data
- `tests/` - Test suite (10 test files)
- `.github/` - GitHub Actions workflows and documentation plots
- `htmlcov/` - Coverage reports (generated)

### Key Files
- `pyproject.toml` - Modern Python packaging configuration with dependencies
- `.pre-commit-config.yaml` - Pre-commit hooks configuration
- `README.md` - Documentation with examples
- `.github/workflows/ci.yaml` - CI pipeline running on Linux/Windows/Mac

## Common Tasks

### Repository Root Contents
```
.
├── .github/            # GitHub workflows and documentation
├── .pre-commit-config.yaml
├── LICENSE
├── README.md           # Main documentation with examples
├── pyproject.toml      # Package configuration and dependencies
├── pysankey/           # Source code
│   ├── __init__.py
│   ├── sankey/         # Core implementation
│   ├── fruits.txt      # Sample data (1041 fruit predictions)
│   └── customers-goods.csv  # Sample customer transaction data
└── tests/              # Test suite (10 test files)
```

### Main Dependencies
Core dependencies (always installed):
- matplotlib>=2.1.0rc1
- numpy>=1.16.5
- pandas
- seaborn>=0.8.1

Test dependencies (installed with `pip install -e ".[test]"`):
- coverage, coveralls
- pre-commit
- pylint>=2.14.5,<3.4
- pytest-cov

### Core Functionality
The main function is `sankey()` which creates Sankey diagrams:
```python
from pysankey import sankey
import matplotlib.pyplot as plt

# Basic usage
ax = sankey(
    left=source_data,      # Source labels
    right=target_data,     # Target labels
    leftWeight=weights,    # Optional weights
    rightWeight=weights,   # Optional weights
    colorDict=colors,      # Optional color mapping
    aspect=20,             # Diagram aspect ratio
    fontsize=12           # Label font size
)
plt.show()  # or plt.savefig()
```

### Troubleshooting

**Network Issues**: The build environment may have network connectivity issues affecting:
- `python -m build` (package building)
- `pre-commit run --all-files` (pre-commit hook installation)
- Solution: Use local tools (`ruff`, `pylint`, `pytest`) instead

**Import Errors**: Always install in development mode:
- Run `pip install -e ".[test]"` from repository root
- Verify with `python -c "from pysankey import sankey; print('✓ Import successful')"`

**Test Failures**: 
- Ensure matplotlib backend is properly set for headless environments
- Use `matplotlib.use('Agg')` for non-interactive environments
- Sample data files must be accessible at `pysankey/fruits.txt` and `pysankey/customers-goods.csv`

**Code Quality**: 
- Use `ruff check --fix .` for automatic fixes
- Use `ruff format .` for code formatting
- Use `pylint pysankey` for comprehensive linting
- All tools should complete in <15 seconds