# Repository Classifier

A Python library for classifying GitHub repositories using both heuristic keyword-based and AI-powered methods.

## Installation

```bash
pip install repo-classifier
```

Or install from source:

```bash
git clone https://github.com/samhsu-dev/repo_classifier.git
cd repo_classifier
pip install -e .
```

## Features

- Classify repositories using keyword-based heuristic method
- Classify repositories using AI services (OpenAI GPT, DeepSeek, etc.)
- Built-in classifiers for PHP, Python, and JavaScript
- Extensible system for custom classifiers
- Multiple ways to define and load classifiers

## Project Structure

```
repo_classifier/
├── src/
│   └── repo_classifier/      # Package (import repo_classifier)
│       ├── __init__.py       # Exports public API
│       ├── core.py           # Core interfaces
│       ├── utils.py          # Utility functions
│       ├── registry.py       # Classifier configuration registry
│       ├── description/      # README classification (heuristic, aimodel)
│       ├── evaluation.py     # Ground truth and evaluation
│       ├── file_type.py      # File-type inference
│       └── predefine/        # Built-in classifiers (php, python, javascript)
├── examples/                 # Example scripts
├── tests/                    # Test directory
├── setup.py                  # Installation configuration
├── requirements.txt          # Dependencies
└── README.md                 # This file
```

## Usage

### Basic Usage

```python
from repo_classifier import classify_repository_heuristic, CLASSIFIER_NAMES

# Use built-in PHP classifier
results = classify_repository_heuristic(
    "https://github.com/user/repo",
    classifier=CLASSIFIER_NAMES.PHP
)
print(results)  # {"Web App": 0.85, "Framework": 0.45, "Library": 0.30}

# Use built-in Python classifier
results = classify_repository_heuristic(
    "https://github.com/user/repo",
    classifier=CLASSIFIER_NAMES.PYTHON
)
print(results)  # {"Web Framework": 0.92, "Library/Package": 0.45}

# Use built-in JavaScript classifier
results = classify_repository_heuristic(
    "https://github.com/user/repo",
    classifier=CLASSIFIER_NAMES.JAVASCRIPT
)
print(results)  # {"Frontend Framework": 0.88, "JavaScript Library": 0.40}
```

### Using AI Classification

```python
from repo_classifier import classify_repository_aimodel, CLASSIFIER_NAMES

# Use AI classification with built-in PHP project types
results = classify_repository_aimodel(
    "https://github.com/user/repo",
    api_key="your_api_key",
    classifier=CLASSIFIER_NAMES.PHP,
    model_name="gpt-3.5-turbo"
)
print(results)
```

### Using CLASSIFIER_NAMES

The `CLASSIFIER_NAMES` object provides a convenient way to access the built-in classifier names:

```python
from repo_classifier import CLASSIFIER_NAMES

# Access individual classifier names
php_classifier = CLASSIFIER_NAMES.PHP       # "php"
python_classifier = CLASSIFIER_NAMES.PYTHON # "python"
js_classifier = CLASSIFIER_NAMES.JAVASCRIPT # "javascript"

# Get a list of all classifier names
all_classifiers = CLASSIFIER_NAMES.all()    # ["php", "python", "javascript"]

# Get a list of available classifier names
available = CLASSIFIER_NAMES.available()    # ["php", "python", "javascript"]
```

### Custom Classifier Definition

```python
from repo_classifier import classify_repository_heuristic, register_classifier

# Define custom classifier
custom_config = {
    "Web Framework": {
        "mvc": 10,
        "web framework": 10,
        "router": 8,
        "controller": 8
    },
    "API Service": {
        "api": 10,
        "rest": 10,
        "json": 8,
        "http": 8
    }
}

# Register custom classifier
register_classifier("custom", custom_config)

# Use registered classifier
results = classify_repository_heuristic(
    "https://github.com/user/repo",
    classifier="custom"
)
print(results)
```

### Loading Classifiers from Python Modules

```python
from repo_classifier import load_classifier_from_module, classify_repository_heuristic

# Import classifiers from a module
load_classifier_from_module("path/to/my_classifiers.py")

# Use imported classifier
results = classify_repository_heuristic(
    "https://github.com/user/repo",
    classifier="data_science"
)
print(results)
```

### Creating Classifiers from Text Files

```python
from repo_classifier import create_classifier_from_file, register_classifier

# Create classifier from text file
game_dev_config = create_classifier_from_file("path/to/game_dev.txt")

# Register classifier
register_classifier("game_dev", game_dev_config)

# Use registered classifier
results = classify_repository_heuristic(
    "https://github.com/user/repo",
    classifier="game_dev"
)
print(results)
```

## Running Tests

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run all tests
pytest

# Run tests with coverage
pytest --cov=repo_classifier
```

## License

MIT
