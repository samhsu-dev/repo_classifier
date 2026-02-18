"""Ground truth management for repository classification."""

import json
from typing import Dict, Optional

_GROUND_TRUTH: Dict[str, str] = {}


def load_ground_truth(filepath: str) -> Dict[str, str]:
    """Load ground truth mappings from file.

    Args:
        filepath: Path to JSON/YAML file.

    Returns:
        Dict mapping repository URLs to known types.

    Raises:
        ValueError: If file format invalid.
    """
    global _GROUND_TRUTH
    try:
        with open(filepath, "r") as f:
            if filepath.endswith(".json"):
                _GROUND_TRUTH = json.load(f)
            else:
                raise ValueError(f"Unsupported file format: {filepath}")
        return _GROUND_TRUTH
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in file {filepath}: {e}")
    except Exception as e:
        raise ValueError(f"Failed to load ground truth file {filepath}: {e}")


def save_ground_truth(filepath: str, truth_dict: Dict[str, str]) -> None:
    """Persist ground truth mappings to file.

    Args:
        filepath: Path to JSON file.
        truth_dict: Repository URLs to known types.
    """
    with open(filepath, "w") as f:
        json.dump(truth_dict, f, indent=2)


def add_ground_truth_entry(repo_url: str, project_type: str) -> None:
    """Add single repository to ground truth registry.

    Args:
        repo_url: GitHub repository URL.
        project_type: Known project type.
    """
    global _GROUND_TRUTH
    _GROUND_TRUTH[repo_url] = project_type


def get_ground_truth_repos() -> Dict[str, str]:
    """Retrieve all ground truth entries.

    Returns:
        Dict mapping repository URLs to known types.
    """
    return _GROUND_TRUTH.copy()


def evaluate_classifier(
    classifier_name: str, truth_dict: Dict[str, str]
) -> Dict[str, float]:
    """Evaluate classifier accuracy against ground truth.

    Args:
        classifier_name: Name of classifier to evaluate.
        truth_dict: Repository URLs to known types.

    Returns:
        Metrics dict (accuracy, precision, recall, F1).
    """
    return {
        "accuracy": 0.0,
        "precision": 0.0,
        "recall": 0.0,
        "f1": 0.0,
    }
