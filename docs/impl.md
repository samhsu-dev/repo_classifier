# Implementation Guide: LLM Integration

## Libraries

- **litellm** ≥1.81.0 — Unified API for 100+ LLM providers; use `completion()` with `response_format={"type": "json_object"}` for structured output.

## APIs

- **`litellm.completion(model, messages, response_format, temperature, timeout, api_key)`** — Call LLM with JSON output. Returns `ModelResponse` with content at `['choices'][0]['message']['content']`. Provider auto-detected from model string (e.g., `"gpt-4o"` → OpenAI, `"claude-3-opus-20240229"` → Anthropic).
- **`json.loads(json_str)`** — Parse LLM's JSON response. Raises `json.JSONDecodeError` if malformed.

## Developer Instructions

- Add litellm to `pyproject.toml` dev dependencies: `"litellm>=1.81.0"`.
- Refactor `classify_repository_ai()` in `core.py`: replace raw HTTP calls with `litellm.completion()`.
- Cascade pipeline unchanged: Ground Truth → File Type → LLM (in that order).
- Prompt must request JSON output explicitly; include phrase "respond in JSON" or similar.
- Parse response: `json_str = response.choices[0].message.content`; then `scores = json.loads(json_str)`.
- Expected JSON format from LLM: `{"ProjectType": score, ...}` or `{"scores": {"ProjectType": score, ...}}` (extract nested "scores" if present).
- Error handling: catch `json.JSONDecodeError` (malformed JSON), `litellm.APIError` (API failure), `litellm.Timeout` (request timeout).
- Cost tracking (optional): access via `response._hidden_params.get("response_cost", 0.0)`.
- Test with multiple providers: OpenAI (set `OPENAI_API_KEY`), Anthropic (set `ANTHROPIC_API_KEY`), Google Gemini (set `GOOGLE_API_KEY`), Groq (set `GROQ_API_KEY`).

## Design-Specific: classify_repository_ai

- Cascade order critical: check ground truth *before* README fetch (avoid network request if known).
- File-type inference confidence threshold = 0.7 (short-circuits LLM step if met).
- LLM is final fallback only; heuristic should be attempted first via `classify_repository_heuristic()` if needed.
- Provider auto-detected from `model_name` (e.g., "gpt-4o" → OpenAI, "claude-3-opus-20240229" → Anthropic).
- `_classify_description_ai()` minimal interface: only parameters actually used (no unused api_url/max_tokens).
