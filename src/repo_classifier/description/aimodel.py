"""Internal LLM-based classification step."""

import json
from typing import Callable, Dict, List, NamedTuple, Optional, Protocol, Union, cast


class _LitellmMessage(Protocol):
    content: str


class _LitellmChoice(Protocol):
    message: _LitellmMessage


class _LitellmResponse(Protocol):
    choices: List[_LitellmChoice]


_litellm_completion_fn: Optional[Callable[..., object]] = None
_litellm_import_error: Optional[ImportError] = None
try:
    from litellm import completion

    _litellm_completion_fn = completion
except ImportError as _exc:
    _litellm_import_error = _exc


class _LLMOptions(NamedTuple):
    """Options for LLM call (model_name, api_key, temperature, timeout)."""

    model_name: str
    api_key: str
    temperature: float = 0.1
    timeout: int = 60


def _classify_description_aimodel(
    readme_text: str,
    classifier: Union[str, List[str]],
    options: _LLMOptions,
    type_descriptions: Optional[Dict[str, str]] = None,
) -> Dict[str, float]:
    """Classify repository using LLM (internal cascade step).

    Formats prompt, calls LLM via litellm, parses JSON response.

    Args:
        readme_text: Raw README text.
        classifier: Classifier name or list of project types.
        options: LLM options (model_name, api_key, temperature, timeout).
        type_descriptions: Optional map of type name -> short description for the prompt.

    Returns:
        Project types to confidence scores (0.0–1.0).

    Raises:
        ValueError: If parameters invalid or LLM call fails.
    """
    if not readme_text:
        raise ValueError("readme_text cannot be empty")
    if not classifier:
        raise ValueError("classifier cannot be empty")
    if _litellm_completion_fn is None:
        assert _litellm_import_error is not None
        raise ValueError(
            "litellm required; install with: pip install litellm"
        ) from _litellm_import_error

    types_list: List[str] = (
        list(classifier) if isinstance(classifier, list) else [classifier]
    )
    descs = type_descriptions or {}
    types_line = "\n".join(
        f"- {t}: {descs[t]}" if t in descs else f"- {t}" for t in types_list
    )
    readme_excerpt = readme_text[:2000].strip()

    system_content = (
        "Classify the repo description into the given types (use type descriptions when provided). "
        "Reply with a single JSON object: keys = type names, values = confidence 0.0–1.0. No other text."
    )
    user_content = f"TYPES:\n{types_line}\n\nDESCRIPTION:\n{readme_excerpt}"

    raw_response = _litellm_completion_fn(
        model=options.model_name,
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content},
        ],
        response_format={"type": "json_object"},
        temperature=options.temperature,
        timeout=options.timeout,
        api_key=options.api_key,
    )
    response = cast(_LitellmResponse, raw_response)

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
