"""
File-type based repository classification.

Analyzes README content for file mentions to infer the most likely project type
with a single confidence score. This is used as the primary classification
method before falling back to heuristic or LLM approaches.
"""

import re
from typing import Dict, List, Optional, Tuple

from .utils import _normalize_scores
from .predefine.file_patterns import _FILE_TYPE_PATTERNS

_TOKEN_RE = re.compile(
    r"""
    [\w./\\-]+          # path-like tokens  (e.g. src/index.js, setup.py)
    \.[\w]+             # must contain an extension or slash
    | [\w-]+\.[\w]+     # simple file names (e.g. package.json)
    | [\w./\\-]+/       # directory refs ending with /
    """,
    re.VERBOSE,
)


def __classify_by_file_type(
    readme_text: str,
    classifier: str,
) -> Optional[Tuple[str, float]]:
    """Infer project type from file patterns in README.

    Internal cascade pipeline step: deterministic file-pattern inference.

    Args:
        readme_text: Raw README content.
        classifier: Classifier name (e.g., 'php', 'python', 'javascript').

    Returns:
        Tuple (project_type_name, confidence_score) or None if no match.

    Raises:
        ValueError: If readme_text is empty.
    """
    if not readme_text:
        raise ValueError("readme_text cannot be empty")

    patterns = _FILE_TYPE_PATTERNS.get(classifier.lower())
    if not patterns:
        return None

    mentioned = __extract_mentioned_files(readme_text)
    if not mentioned:
        return None

    raw_scores = __score_by_file_patterns(mentioned, patterns)
    if not raw_scores or max(raw_scores.values()) == 0:
        return None

    best_type = max(raw_scores.items(), key=lambda x: x[1])
    normalised = _normalize_scores(raw_scores)
    best_score = normalised[best_type[0]]

    return (best_type[0], best_score)


def __extract_mentioned_files(readme_text: str) -> List[str]:
    """Extract file-name and path-like tokens from README text."""
    return [tok.lower() for tok in _TOKEN_RE.findall(readme_text)]


def __score_by_file_patterns(
    mentioned: List[str],
    file_patterns: Dict[str, List[str]],
) -> Dict[str, float]:
    """Score each project type by counting pattern hits in mentioned files."""
    scores: Dict[str, float] = {}
    for project_type, patterns in file_patterns.items():
        hits = 0
        for pattern in patterns:
            pattern_lower = pattern.lower()
            for token in mentioned:
                if pattern_lower in token or token in pattern_lower:
                    hits += 1
                    break
        scores[project_type] = float(hits)
    return scores
