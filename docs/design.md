# Repository Classifier: Design Specification

## Design Overview

### API Classification

**Public API:**
- Classification entry points: `classify_repository_heuristic()`, `classify_repository_aimodel()`
- Classifier management: `register_classifier()`, `get_classifier()`, `get_available_classifiers()`, `unregister_classifier()`, `load_classifier_from_module()`, `create_classifier_from_file()`
- Ground truth management: `load_ground_truth()`, `save_ground_truth()`, `get_ground_truth_repos()`, `add_ground_truth_entry()`, `evaluate_classifier()`
- Predefined classifiers: `CLASSIFIERS` (singleton with `.php`, `.python`, `.javascript`, `.names()`), `PHP`, `PYTHON`, `JAVASCRIPT` (LangClassifier instances). Legacy: `CLASSIFIER_NAMES`, `ALL_PROJECT_TYPES`, `DFT_PROJECT_TYPE_NAMES` (derived from CLASSIFIERS).

**Internal API (single underscore prefix):**
- Low-level classifiers: `_classify_description_heuristic()`, `_classify_description_aimodel()`
- Utilities: `_get_repo_readme()`, `_normalize_scores()`, `_get_top_n_scores()`
- Predefine: single file `predefine.py`; `LangClassifier` constructor takes JSON path only; attributes `name`, `type_keywords`, `type_files`, `type_descriptions`, `type_names`. Built-ins load from `data/php.json`, `data/python.json`, `data/javascript.json`. File-type inference uses `_FILE_TYPE_PATTERNS` (built from CLASSIFIERS).

**Private Implementation (double underscore prefix, never exposed):**
- File type inference: `__classify_by_file_type()` — Used only by cascade pipeline internally
- Private helpers: `__extract_mentioned_files()`, `__score_by_file_patterns()`

### Dependency Roles

- **Orchestrators**: `classify_repository_heuristic`, `classify_repository_aimodel` (implement cascade pipeline)
- **Helpers**: `_classify_description_heuristic()`, `_classify_description_aimodel()`, `_get_repo_readme()` (receive inputs by argument, stateless)
- **Data Holders**: Ground truth registry, classifier configs (keyword weights), file patterns
- **Dependencies**: One-way only (Orchestrators → Helpers); no circular dependencies

---

## Function Specifications

### Public API

#### `classify_repository_heuristic(repo_url: str, classifier: Union[str, Dict[str, Dict[str, int]], LangClassifier], top_n: int = 3) -> Dict[str, float]`

Responsibility: Main entry point implementing cascade pipeline (Ground Truth → File Type → Heuristic).

Behavior:
1. Validate inputs (URL, classifier, top_n)
2. Check ground truth (highest priority); if found, return {type: 1.0}
3. Fetch README content (only if ground truth check fails)
4. Attempt file-type inference via internal file-type classifier (when classifier is a LangClassifier or resolved by name)
5. If file result has confidence >= 0.7, return immediately
6. Otherwise, fall back to heuristic classification
7. Apply top-N filtering and return

Input:
- `repo_url`: GitHub repository URL (non-empty string)
- `classifier`: LangClassifier instance (e.g. `PHP`, `CLASSIFIERS.php`), classifier name (str), or inline config dict (non-empty)
- `top_n`: Positive integer for result count (default: 3)

Output: `Dict[str, float]` — top-N project types to scores (0.0–1.0)

Errors: Raises `ValueError` for invalid parameters.

Example:
```python
from repo_classifier import classify_repository_heuristic, PHP
results = classify_repository_heuristic(
    "https://github.com/laravel/laravel",
    PHP,  # or CLASSIFIERS.php or "php"
    top_n=3
)
# {"Framework": 0.95, "Web App": 0.04, "Library": 0.01}
```

---

#### `classify_repository_aimodel(repo_url: str, classifier: Union[str, List[str], LangClassifier], model_name: str, api_key: str, top_n: int = 3, temperature: float = 0.1, timeout: int = 60) -> Dict[str, float]`

Responsibility: LLM-based classification path using cascade pipeline (Ground Truth → File Type → LLM).

Behavior:
1. Validate all parameters
2. Check ground truth (highest priority); if found, return {type: 1.0}
3. Fetch README content
4. Attempt file-type inference; if confident (>= 0.7 threshold), return
5. Otherwise, call LLM via litellm.completion() with response_format={"type": "json_object"}
6. Parse JSON response and apply top-N filtering

Input:
- `repo_url`: GitHub repository URL
- `classifier`: LangClassifier (e.g. `CLASSIFIERS.python`), classifier name (str), or list of project type names
- `model_name`: Full model id in form `provider/model` (e.g. "openai/gpt-4o", "deepseek/deepseek-chat", "anthropic/claude-3-opus-20240229")
- `api_key`: API credentials
- `top_n`: Number of top results (default: 3)
- `temperature`: LLM randomness 0.0–1.0 (default: 0.1)
- `timeout`: Request timeout in seconds (default: 60)

Output: `Dict[str, float]` — project types to scores (0.0–1.0)

Errors: Raises `ValueError` for invalid params, network failures, or JSON parse errors.

Example:
```python
from repo_classifier import classify_repository_aimodel, CLASSIFIERS
results = classify_repository_aimodel(
    "https://github.com/django/django",
    CLASSIFIERS.python,  # or ["Web Framework", "Library", "Tool"] or "python"
    model_name="openai/gpt-4o",
    api_key="sk-...",
)
```

---

#### `register_classifier(name: str, config: Dict[str, Dict[str, int]]) -> None`

Responsibility: Add classifier to registry.

Input: Classifier name, keyword-weight configuration dict

Errors: None (silently overwrites if exists)

---

#### `get_classifier(name: str) -> Optional[Dict[str, Dict[str, int]]]`

Responsibility: Retrieve classifier from registry by name.

Input: Classifier name (case-insensitive)

Output: Config dict or None if not found

---

#### `get_available_classifiers() -> List[str]`

Responsibility: List all registered classifier names.

Output: List of classifier names

---

#### `unregister_classifier(name: str) -> bool`

Responsibility: Remove classifier from registry.

Input: Classifier name

Output: True if removed, False if not found

---

#### `load_classifier_from_module(module_path: str, attribute_name: Optional[str] = None) -> str`

Responsibility: Import classifier from Python module.

Input: Path to Python module, optional variable name

Output: Registered classifier name

---

#### `create_classifier_from_file(file_path: str, encoding: str = 'utf-8') -> Dict[str, Dict[str, int]]`

Responsibility: Load classifier from text file.

Input: File path, encoding

Output: Parsed configuration dict

---

#### `load_ground_truth(filepath: str) -> Dict[str, str]`

Responsibility: Load ground truth mappings from file.

Input: File path

Output: Dict mapping repository URLs to known types

Errors: Raises `ValueError` for invalid file format

---

#### `save_ground_truth(filepath: str, truth_dict: Dict[str, str]) -> None`

Responsibility: Persist ground truth mappings to file.

Input: File path, ground truth dict

Output: None (file written)

---

#### `evaluate_classifier(classifier_name: str, truth_dict: Dict[str, str]) -> Dict[str, float]`

Responsibility: Evaluate classifier accuracy against ground truth.

Input: Classifier name, ground truth dict

Output: Metrics dict (accuracy, precision, recall, F1)

---

#### `add_ground_truth_entry(repo_url: str, project_type: str) -> None`

Responsibility: Add single repository to ground truth registry.

Input: Repository URL, known project type

Output: None (registry updated)

---

#### `get_ground_truth_repos() -> Dict[str, str]`

Responsibility: Retrieve all ground truth entries.

Output: Dict mapping repository URLs to known types

---

### Internal API

#### `_classify_description_heuristic(readme_text: str, classifier: Union[str, Dict]) -> Dict[str, float]`

Responsibility: Keyword-based fallback classification (internal cascade step).

Behavior: Scan README for keywords; aggregate weights; normalize scores.

Input: Raw README text, classifier name or config dict

Output: All project types with normalised scores (0.0–1.0)

Errors: Raises `ValueError` if readme_text is empty

---

#### `_classify_description_aimodel(readme_text: str, classifier: Union[str, List[str]], model_name: str, api_key: str, temperature: float = 0.1, timeout: int = 60) -> Dict[str, float]`

Responsibility: Internal LLM-based classification step (uses litellm).

Behavior: Format prompt, call LLM, parse JSON response.

Input: README text, classifier name/types, model name, API key, temperature, timeout.

Output: Project types with confidence scores (0.0–1.0).

Errors: Raises `ValueError` for invalid parameters or LLM failures.

---

#### `_get_repo_readme(repo_url: str) -> str`

Responsibility: Fetch README from GitHub.

Input: GitHub repository URL

Output: README content as plaintext string

Errors: Raises `ValueError` for invalid URL or network failures

---

#### `_normalize_scores(scores: Dict[str, float]) -> Dict[str, float]`

Responsibility: Normalize raw scores to 0.0–1.0 range.

Input: Dict of raw scores

Output: Dict of normalized scores (0.0–1.0)

---

#### `_get_top_n_scores(scores: Dict[str, float], n: int) -> Dict[str, float]`

Responsibility: Filter and rank top N scores.

Input: Dict of scores, positive integer N

Output: Dict with at most N entries sorted by score descending

---

#### File patterns (LangClassifier.type_files)

Data: Each LangClassifier exposes `type_files` (loaded from a JSON file in `data/`): a dict mapping type names to lists of file/path pattern strings. `predefine.py` exposes `_FILE_TYPE_PATTERNS` (classifier name → type_files) built from CLASSIFIERS; file_type.py uses it in `__classify_by_file_type()`.

---

### Private Implementation

#### `__classify_by_file_type(readme_text: str, classifier: str) -> Optional[Tuple[str, float]]`

Responsibility: File-pattern-based type inference step in cascade pipeline.

Behavior: Extract tokens, score types, return highest or None if low confidence

Usage: Called by `classify_repository_heuristic()` and `classify_repository_aimodel()` internally

Note: NOT exposed in public API; uses `__` prefix for name mangling

---

## Exception / Error Types

| Exception | When Raised |
|-----------|------------|
| `ValueError("Repository URL cannot be empty")` | `repo_url` is falsy in public functions |
| `ValueError("Classifier cannot be empty")` | `classifier` is falsy |
| `ValueError("top_n must be a positive integer")` | `top_n <= 0` |
| `ValueError("Classifier not found: ...")` | String classifier not in registry |
| `ValueError("README not found for repository: ...")` | GitHub returns 404 for README |
| `ValueError("Network error when fetching README...")` | Network failure during README fetch |
| `ValueError("Invalid JSON from LLM")` | LLM returned malformed JSON |

---

## Validation Rules

### Public API Validation

**classify_repository_heuristic:**
- `repo_url` must be non-empty string matching GitHub URL format
- `classifier` must be non-empty string (registry lookup) or non-empty dict (inline config)
- `top_n` must be positive integer

**classify_repository_aimodel:**
- `repo_url`, `classifier`, `model_name`, `api_key` must be non-empty
- `top_n` must be positive integer
- `temperature` must be in [0.0, 1.0]
- `timeout` must be positive integer

**registry functions:**
- `register_classifier`: `name` must be non-empty; case-insensitive lookup
- `register_classifier`: `config` must be non-empty dict with project-type keys
- `get_classifier`: Case-insensitive; returns None if not found
- `get_available_classifiers`: Returns list of all registered names

**evaluation functions:**
- `load_ground_truth`: File must be valid JSON or YAML format
- `save_ground_truth`: Creates/overwrites file at specified path
- `evaluate_classifier`: Returns dict with metrics
- `add_ground_truth_entry`: Updates in-memory registry

---

## Cascade Pipeline Logic

**Priority Order (highest to lowest):**
1. **Ground Truth** — If repository URL in ground truth registry, return {type: 1.0} immediately (no README fetch)
2. **File Type Inference** — If file patterns produce confidence >= 0.7, return that result (short-circuit to avoid fallback)
3. **Heuristic Classification** — Keyword-based fallback when file inference uncertain
4. **LLM Classification** — Used only via `classify_repository_aimodel()`; alternative path to heuristic (not sequential)

**File Type Confidence Threshold:** 0.7

**Network Efficiency:** Ground truth check before README fetch eliminates unnecessary network requests for known repositories.

**Short-Circuit Behavior:** Once a stage returns result with sufficient confidence, later stages skipped.
