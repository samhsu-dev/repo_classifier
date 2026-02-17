"""
Heuristic-based classification functionality.

This module provides keyword-based classification for repositories using a heuristic approach.
It analyzes README content to determine the most likely project types based on keyword frequency
and predefined weights.
"""

from typing import Dict, Union
from ..utils import _normalize_scores

def _classify_description_heuristic(
    readme_text: str, classifier: Union[str, Dict[str, Dict[str, int]]], 
) -> Dict[str, float]:
    """Keyword-based fallback classification (internal cascade step).

    Scans README for keywords; aggregates weights; normalizes scores.

    Args:
        readme_text: Raw README text.
        classifier: Classifier config dict or name string.

    Returns:
        All project types with normalised scores (0.0–1.0).

    Raises:
        ValueError: If readme_text empty or classifier invalid.
    """
    if not readme_text:
        raise ValueError("readme_text cannot be empty")

    processed_text = readme_text.lower()
    scores = {}
    for project_type, keywords in classifier.items():
        type_score = 0
        for keyword, weight in keywords.items():
            occurrences = processed_text.count(keyword.lower())
            type_score += occurrences * weight
        scores[project_type] = type_score

    return _normalize_scores(scores)
