"""README processing module for low-level classification."""

from .heuristic import _classify_description_heuristic
from .aimodel import _classify_description_aimodel

__all__ = [
    '_classify_description_heuristic',
    '_classify_description_aimodel'
]
