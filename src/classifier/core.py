"""Core functionality for repository classification.

Implements cascade pipeline: Ground Truth → File Type → Heuristic/LLM.
"""

from typing import Dict, List, Optional, Union

from .description import (
    _classify_description_aimodel,
    _classify_description_heuristic,
    _LLMOptions,
)
from .evaluation import get_ground_truth_repos
from .file_type import __classify_by_file_type
from .predefine import DFT_PROJECT_TYPE_NAMES
from .predefine.base import LanguageClassifier
from .registry import get_available_classifiers, get_classifier
from .utils import _get_repo_readme, _get_top_n_scores

__all__ = [
    "classify_repository_heuristic",
    "classify_repository_aimodel",
]

# File-type inference confidence threshold: if >= this value, return directly
FILE_TYPE_CONFIDENCE_THRESHOLD = 0.7


def classify_repository_heuristic(
    repo_url: str,
    classifier: Union[str, Dict[str, Dict[str, int]], LanguageClassifier],
    top_n: int = 3,
) -> Dict[str, float]:
    """Classify a GitHub repository using cascade pipeline.

    Priority order:
    1. Ground Truth (if repository is in the ground truth registry)
    2. File Type Inference (if confidence >= threshold)
    3. Heuristic (default fallback)

    Args:
        repo_url: GitHub repository URL.
        classifier: Classifier name, config dict, or LanguageClassifier (e.g. CLASSIFIERS.php).
        top_n: Number of top types to return. Must be positive.

    Returns:
        Mapping of project types to confidence scores (0.0–1.0).

    Raises:
        ValueError: If required parameters are invalid.
    """
    if not repo_url:
        raise ValueError("Repository URL cannot be empty")
    if not classifier:
        raise ValueError("Classifier cannot be empty")
    if top_n <= 0:
        raise ValueError("top_n must be a positive integer")

    # Normalize: LanguageClassifier -> name + config
    if isinstance(classifier, LanguageClassifier):
        classifier_name = classifier.name
        config = classifier.project_types
    elif isinstance(classifier, str):
        classifier_name = classifier
        _config = get_classifier(classifier)
        if _config is None:
            available = get_available_classifiers()
            raise ValueError(
                f"Classifier not found: {classifier}. "
                f"Available classifiers: {', '.join(available)}"
            )
        config = _config
    else:
        classifier_name = None
        config = classifier

    # Step 1: Check ground truth (highest priority)
    if classifier_name and classifier_name in DFT_PROJECT_TYPE_NAMES:
        ground_truth = get_ground_truth_repos()
        true_type = ground_truth.get(repo_url)
        if true_type:
            return {true_type: 1.0}

    # Step 2: Get README
    readme_text = _get_repo_readme(repo_url)

    # Step 3: Try file-type inference (primary deterministic method)
    if classifier_name:
        file_result = __classify_by_file_type(readme_text, classifier_name)
        if file_result and file_result[1] >= FILE_TYPE_CONFIDENCE_THRESHOLD:
            return {file_result[0]: file_result[1]}

    # Step 4: Fall back to heuristic (default)
    all_scores = _classify_description_heuristic(readme_text, config)
    return _get_top_n_scores(all_scores, top_n)


def classify_repository_aimodel(
    repo_url: str,
    classifier: Union[str, List[str], LanguageClassifier],
    model_name: str,
    api_key: str,
    top_n: int = 3,
    temperature: float = 0.1,
    timeout: int = 60,
) -> Dict[str, float]:
    """Classify repository using LLM (cascade pipeline: Ground Truth → File Type → LLM).

    Args:
        repo_url: GitHub repository URL.
        classifier: Classifier name (str), list of project types, or LanguageClassifier.
        model_name: LLM model identifier (e.g., "gpt-4o", "claude-3-opus-20240229").
        api_key: API credentials.
        top_n: Number of top results (default: 3).
        temperature: LLM randomness 0.0–1.0 (default: 0.1).
        timeout: Request timeout in seconds (default: 60).

    Returns:
        Dict[str, float] — project types to confidence scores (0.0–1.0).

    Raises:
        ValueError: For invalid parameters, network failures, or JSON parse errors.
    """
    if not repo_url:
        raise ValueError("Repository URL cannot be empty")
    if not classifier:
        raise ValueError("Classifier cannot be empty")
    if top_n <= 0:
        raise ValueError("top_n must be a positive integer")
    if temperature < 0.0 or temperature > 1.0:
        raise ValueError("temperature must be between 0.0 and 1.0")
    if timeout <= 0:
        raise ValueError("timeout must be a positive integer")
    if not api_key:
        raise ValueError("API key cannot be empty")
    if not model_name:
        raise ValueError("Model name cannot be empty")

    # Normalize: LanguageClassifier -> name + project_type_names list
    _name: Optional[str]
    _project_types: Union[str, List[str]]
    if isinstance(classifier, LanguageClassifier):
        _name = classifier.name
        _project_types = classifier.project_type_names
    else:
        _name = classifier if isinstance(classifier, str) else None
        _project_types = classifier

    # Step 1: Check ground truth
    if _name and _name in DFT_PROJECT_TYPE_NAMES:
        ground_truth = get_ground_truth_repos()
        true_type = ground_truth.get(repo_url)
        if true_type:
            return {true_type: 1.0}

    # Step 2: Get README
    readme_text = _get_repo_readme(repo_url)

    # Step 3: Try file-type inference
    if _name:
        file_result = __classify_by_file_type(readme_text, _name)
        if file_result and file_result[1] >= FILE_TYPE_CONFIDENCE_THRESHOLD:
            return {file_result[0]: file_result[1]}

    # Step 4: Fall back to LLM classification
    options = _LLMOptions(
        model_name=model_name,
        api_key=api_key,
        temperature=temperature,
        timeout=timeout,
    )
    scores = _classify_description_aimodel(
        readme_text=readme_text,
        classifier=_project_types,
        options=options,
    )
    return _get_top_n_scores(scores, top_n)
