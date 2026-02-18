"""Utility functions for repository classification."""

from typing import Dict

import requests


def _normalize_scores(scores: Dict[str, float]) -> Dict[str, float]:
    """Normalize scores to 0.0–1.0 range by dividing by maximum.

    Args:
        scores: Dict of raw scores.

    Returns:
        Dict with normalized scores in [0.0, 1.0]. Empty dict if input empty.
    """
    if not scores:
        return {}

    max_score = max(scores.values())
    if max_score == 0:
        return {k: 0.0 for k in scores}

    return {k: v / max_score for k, v in scores.items()}


def _get_top_n_scores(scores: Dict[str, float], n: int) -> Dict[str, float]:
    """Return top N highest-scoring entries.

    Args:
        scores: Dict of scores.
        n: Positive integer for number of top entries.

    Returns:
        Dict with at most N entries, sorted by score descending.
    """
    if n <= 0:
        return {}
    sorted_items = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return dict(sorted_items[:n])


def _get_repo_readme(repo_url: str) -> str:
    """Fetch README content from GitHub repository.

    Tries multiple README filename and branch variants.

    Args:
        repo_url: GitHub repository URL.

    Returns:
        README content as plaintext string.

    Raises:
        ValueError: If URL invalid, README not found, or network error.
    """
    if not repo_url.startswith("https://github.com/"):
        raise ValueError(f"Invalid GitHub repository URL: {repo_url}")

    repo_path = repo_url.replace("https://github.com/", "")
    parts = repo_path.split("/")
    if len(parts) < 2:
        raise ValueError(f"Invalid repository URL format: {repo_url}")

    owner, repo = parts[0], parts[1]

    # GitHub raw URLs are case-sensitive; repos use README.md, Readme.md, readme.md, etc.
    readme_filenames = [
        "README.md",
        "Readme.md",
        "readme.md",
        "README.rst",
        "Readme.rst",
        "README",
    ]
    branches = ["main", "master"]
    readme_variants = [
        f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{filename}"
        for branch in branches
        for filename in readme_filenames
    ]

    for url in readme_variants:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return response.text
        except requests.RequestException:
            continue

    raise ValueError(f"README not found for repository: {repo_url}")
