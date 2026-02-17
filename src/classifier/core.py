"""Core functionality for repository classification.

Implements cascade pipeline: Ground Truth → File Type → Heuristic/LLM.
"""

from typing import Dict, List, Optional, Union

from .registry import get_classifier, get_available_classifiers
from .utils import _get_top_n_scores, _get_repo_readme
from .description import _classify_description_heuristic, _classify_description_aimodel
from .predefine import DFT_PROJECT_TYPE_NAMES
from .evaluation import get_ground_truth_repos
from .file_type import __classify_by_file_type

__all__ = [
    'classify_repository_heuristic',
    'classify_repository_aimodel',
]

# File-type inference confidence threshold: if >= this value, return directly
FILE_TYPE_CONFIDENCE_THRESHOLD = 0.7

def classify_repository_heuristic(
    repo_url: str,
    classifier: Union[str, Dict[str, Dict[str, int]]],
    top_n: int = 3,
) -> Dict[str, float]:
    """Classify a GitHub repository using cascade pipeline.

    Priority order:
    1. Ground Truth (if repository is in the ground truth registry)
    2. File Type Inference (if confidence >= threshold)
    3. Heuristic (default fallback)

    Args:
        repo_url: GitHub repository URL.
        classifier: Classifier name or configuration dict.
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

    # Step 1: Check ground truth (highest priority)
    if classifier in DFT_PROJECT_TYPE_NAMES:
        ground_truth = get_ground_truth_repos()
        true_type = ground_truth.get(repo_url)
        if true_type:
            return {true_type: 1.0}

    # Resolve classifier to config if it's a string
    if isinstance(classifier, str):
        config = get_classifier(classifier)
        if not config:
            available = get_available_classifiers()
            raise ValueError(
                f"Classifier not found: {classifier}. "
                f"Available classifiers: {', '.join(available)}"
            )
        classifier_name = classifier
    else:
        config = classifier
        classifier_name = None

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
    classifier: Union[str, List[str]],
    api_url: str,
    model_name: str,
    api_key: str,
    top_n: int = 3,
    temperature: float = 0.1,
    max_in_tokens: Optional[int] = None,
    max_out_tokens: Optional[int] = None,
    timeout: int = 60,
) -> Dict[str, float]:
    """Classify repository using LLM (cascade pipeline: Ground Truth → File Type → LLM).

    Args:
        repo_url: GitHub repository URL.
        classifier: Classifier name (str) or list of project types.
        api_url: LLM service endpoint.
        model_name: LLM model identifier (e.g., "gpt-4o", "claude-3-opus-20240229").
        api_key: API credentials.
        top_n: Number of top results (default: 3).
        temperature: LLM randomness 0.0–1.0 (default: 0.1).
        max_in_tokens: Input token limit (optional).
        max_out_tokens: Output token limit (optional).
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

    # Step 1: Check ground truth
    if isinstance(classifier, str) and classifier in DFT_PROJECT_TYPE_NAMES:
        ground_truth = get_ground_truth_repos()
        true_type = ground_truth.get(repo_url)
        if true_type:
            return {true_type: 1.0}

    # Step 2: Get README
    readme_text = _get_repo_readme(repo_url)

    # Step 3: Try file-type inference
    if isinstance(classifier, str):
        file_result = __classify_by_file_type(readme_text, classifier)
        if file_result and file_result[1] >= FILE_TYPE_CONFIDENCE_THRESHOLD:
            return {file_result[0]: file_result[1]}

    # Step 4: Fall back to LLM classification
    scores = _classify_description_aimodel(
        readme_text=readme_text,
        classifier=classifier,
        model_name=model_name,
        api_key=api_key,
        temperature=temperature,
        timeout=timeout,
    )
    return _get_top_n_scores(scores, top_n)