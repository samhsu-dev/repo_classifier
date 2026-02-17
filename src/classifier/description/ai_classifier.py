"""Internal LLM-based classification step."""

import json
from typing import Dict, List, Union


def _classify_description_aimodel(
    readme_text: str,
    classifier: Union[str, List[str]],
    model_name: str,
    api_key: str,
    temperature: float = 0.1,
    timeout: int = 60,
) -> Dict[str, float]:
    """Classify repository using LLM (internal cascade step).

    Formats prompt, calls LLM via litellm, parses JSON response.

    Args:
        readme_text: Raw README text.
        classifier: Classifier name or list of project types.
        model_name: LLM model identifier.
        api_key: API credentials.
        temperature: LLM randomness 0.0–1.0.
        timeout: Request timeout in seconds.

    Returns:
        Project types to confidence scores (0.0–1.0).

    Raises:
        ValueError: If parameters invalid or LLM call fails.
    """
    if not readme_text:
        raise ValueError("readme_text cannot be empty")
    if not classifier:
        raise ValueError("classifier cannot be empty")

    try:
        from litellm import completion
    except ImportError:
        raise ValueError("litellm required; install with: pip install litellm")

    project_types_str = ", ".join(classifier) if isinstance(classifier, list) else classifier

    prompt = (
        f"Classify this GitHub README into one of these project types: {project_types_str}\n\n"
        f"README:\n{readme_text[:2000]}"
    )

    response = completion(
        model=model_name,
        messages=[
            {
                "role": "system",
                "content": "You are a repository classifier. Respond with valid JSON only.",
            },
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"},
        temperature=temperature,
        timeout=timeout,
        api_key=api_key,
    )

    try:
        json_str = response.choices[0].message.content
    except (AttributeError, IndexError, KeyError, TypeError) as e:
        raise ValueError(f"LLM response missing message content: {e}") from e

    try:
        result = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"LLM returned invalid JSON: {e}") from e

    scores = result.get("scores", result)
    if not isinstance(scores, dict):
        raise ValueError("Invalid JSON structure from LLM")

    return scores
