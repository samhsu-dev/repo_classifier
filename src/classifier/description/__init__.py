"""README processing module for low-level classification."""

from .heuristic import _classify_description_heuristic
from .ai_classifier import _classify_description_ai

__all__ = [
    '_classify_description_heuristic',
    '_classify_description_ai'
]
