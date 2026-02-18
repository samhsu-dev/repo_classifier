# Repository Classifier

Classifies GitHub repositories by project type using a cascade: **Ground Truth → File-type inference → Heuristic or LLM**. Built-in classifiers: PHP, Python, JavaScript.

## Installation

```bash
pip install repo-classifier
```

From source (uses [uv](https://docs.astral.sh/uv/)):

```bash
git clone https://github.com/samhsu-dev/repo_classifier.git
cd repo_classifier
uv sync
```

## Usage

```python
from repo_classifier import classify_repository_heuristic, classify_repository_aimodel, CLASSIFIERS

# Heuristic (no API key)
results = classify_repository_heuristic(
    "https://github.com/laravel/laravel",
    classifier=CLASSIFIERS.php,  # or "php"
    top_n=3,
)
# {"Framework": 0.95, ...}

# LLM: set api_key and model_name (provider/model, e.g. openai/gpt-4o); optional: docs/.env (see docs/.env.example)
results = classify_repository_aimodel(
    "https://github.com/django/django",
    classifier=CLASSIFIERS.python,
    model_name="openai/gpt-4o",
    api_key="sk-...",
)
```

## Advanced usage

**Custom classifier** — register a name → type/weight map; then pass the name to `classify_repository_heuristic` or `classify_repository_aimodel`.

```python
from repo_classifier import register_classifier, classify_repository_heuristic

register_classifier("game", {"Game Engine": {"engine": 10, "game": 8}, "Tool": {"editor": 10}})
classify_repository_heuristic("https://github.com/...", classifier="game", top_n=2)
```

**Classifier from file or module** — File format: `TYPE: TypeName` then `keyword: weight` per line. `create_classifier_from_file(path)` returns a config dict; pass to classification or `register_classifier`. `load_classifier_from_module(module_path, attribute_name=None)` registers config(s) from a module.

```python
from repo_classifier import create_classifier_from_file, register_classifier, load_classifier_from_module

config = create_classifier_from_file("path/to/types.txt")
register_classifier("my_domain", config)
# or: load_classifier_from_module("path/to/classifiers.py")
```

**LLM with custom type list** — pass a list of type names; no registration.

```python
classify_repository_aimodel(
    "https://github.com/...",
    classifier=["Web App", "API", "Library", "CLI"],
    model_name="openai/gpt-4o-mini",
    api_key="sk-...",
)
```

**Ground truth and evaluation** — `load_ground_truth(path)` / `save_ground_truth(path, dict)`; `add_ground_truth_entry(url, type)`; `evaluate_classifier(name, truth_dict)` returns metrics (accuracy, precision, recall, f1).

```python
from repo_classifier import load_ground_truth, evaluate_classifier

truth = load_ground_truth("path/to/ground_truth.json")
metrics = evaluate_classifier("php", truth)
```

## Documentation

| Doc | Purpose |
|-----|--------|
| [docs/demo.ipynb](docs/demo.ipynb) | End-to-end demo; configure via `docs/.env` (see [docs/.env.example](docs/.env.example)) |
| [docs/idea.md](docs/idea.md) | Concepts, architecture, data flow, cascade pipeline, scenarios |
| [docs/design.md](docs/design.md) | Public/internal API, validation, errors, cascade behaviour |
| [docs/impl.md](docs/impl.md) | LLM integration (litellm), prompt and response handling |

## Development

Uses [uv](https://docs.astral.sh/uv/). From the repo root:

```bash
uv sync
uv run pytest
uv run pytest --cov=repo_classifier
```

Lint/format: `uv run black`, `uv run isort`, `uv run mypy`, `uv run pylint` (see `pyproject.toml`).

## License

MIT
