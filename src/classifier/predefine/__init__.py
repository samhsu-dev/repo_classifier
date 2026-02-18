"""
Project type classifiers module.

Uses singleton + property: one list of LanguageClassifier instances drives
all derived data. To add a language: add a LanguageClassifier instance and
append it to the list in _BuiltinClassifiers._classifiers.
"""

from typing import Dict, List

from .base import LanguageClassifier
from .php import PHP
from .python import PYTHON
from .javascript import JAVASCRIPT


class _BuiltinClassifiers:
    """Singleton holding built-in language classifiers. All data via properties."""

    def __init__(self) -> None:
        self._classifiers: List[LanguageClassifier] = [PHP, PYTHON, JAVASCRIPT]

    @property
    def all_project_types(self) -> Dict[str, Dict[str, Dict[str, int]]]:
        return {c.name: c.project_types for c in self._classifiers}

    @property
    def dft_project_type_names(self) -> Dict[str, List[str]]:
        return {c.name: c.project_type_names for c in self._classifiers}

    @property
    def file_type_patterns(self) -> Dict[str, Dict[str, List[str]]]:
        return {c.name: c.file_patterns for c in self._classifiers}

    def names(self) -> List[str]:
        return [c.name for c in self._classifiers]

    @property
    def php(self) -> LanguageClassifier:
        return PHP

    @property
    def python(self) -> LanguageClassifier:
        return PYTHON

    @property
    def javascript(self) -> LanguageClassifier:
        return JAVASCRIPT


CLASSIFIERS = _BuiltinClassifiers()

# Derived from singleton (no standalone constants). Registry/core/file_type use these.
ALL_PROJECT_TYPES = CLASSIFIERS.all_project_types
DFT_PROJECT_TYPE_NAMES = CLASSIFIERS.dft_project_type_names
_FILE_TYPE_PATTERNS = CLASSIFIERS.file_type_patterns


class CLASSIFIER_NAMES:
    """Backward-compat: string names and helpers. Prefer CLASSIFIERS.php.name, CLASSIFIERS.names()."""

    PHP = CLASSIFIERS.php.name
    PYTHON = CLASSIFIERS.python.name
    JAVASCRIPT = CLASSIFIERS.javascript.name

    @classmethod
    def all(cls) -> List[str]:
        return CLASSIFIERS.names()

    @classmethod
    def available(cls) -> List[str]:
        return list(CLASSIFIERS.all_project_types.keys())
