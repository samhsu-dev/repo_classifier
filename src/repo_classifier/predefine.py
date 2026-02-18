"""
Built-in lang classifiers loaded from data/*.json.
To add a language: add a JSON file under data/ and append to _BuiltinClassifiers._classifiers.
"""

import json
import os
from typing import Dict, List


class LangClassifier:
    """Project types loaded from a JSON file.

    JSON format: type name -> {description, keywords, file_patterns}.
    Only JSON file path is accepted.
    """

    def __init__(self, name: str, config_path: str) -> None:
        self._name = name
        with open(config_path, "r", encoding="utf-8") as f:
            self._config = json.load(f)

    @property
    def name(self) -> str:
        return self._name

    @property
    def type_keywords(self) -> Dict[str, Dict[str, int]]:
        """Map type name -> keyword -> weight for heuristic classification."""
        return {k: v.get("keywords", {}) for k, v in self._config.items()}

    @property
    def type_files(self) -> Dict[str, List[str]]:
        """Map type name -> list of file/path patterns for file-type inference."""
        return {k: v.get("file_patterns", []) for k, v in self._config.items()}

    @property
    def type_descriptions(self) -> Dict[str, str]:
        """Map type name -> short description. Used in LLM prompt."""
        return {k: v.get("description", "") for k, v in self._config.items()}

    @property
    def type_names(self) -> List[str]:
        """Ordered list of type names."""
        return list(self._config.keys())


_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
PHP = LangClassifier("php", os.path.join(_DATA_DIR, "php.json"))
PYTHON = LangClassifier("python", os.path.join(_DATA_DIR, "python.json"))
JAVASCRIPT = LangClassifier("javascript", os.path.join(_DATA_DIR, "javascript.json"))


class _BuiltinClassifiers:
    """Singleton holding built-in lang classifiers."""

    def __init__(self) -> None:
        self._classifiers: List[LangClassifier] = [PHP, PYTHON, JAVASCRIPT]

    @property
    def all_project_types(self) -> Dict[str, Dict[str, Dict[str, int]]]:
        return {c.name: c.type_keywords for c in self._classifiers}

    @property
    def dft_project_type_names(self) -> Dict[str, List[str]]:
        return {c.name: c.type_names for c in self._classifiers}

    @property
    def file_type_patterns(self) -> Dict[str, Dict[str, List[str]]]:
        return {c.name: c.type_files for c in self._classifiers}

    def names(self) -> List[str]:
        return [c.name for c in self._classifiers]

    @property
    def php(self) -> LangClassifier:
        return PHP

    @property
    def python(self) -> LangClassifier:
        return PYTHON

    @property
    def javascript(self) -> LangClassifier:
        return JAVASCRIPT


CLASSIFIERS = _BuiltinClassifiers()
ALL_PROJECT_TYPES = CLASSIFIERS.all_project_types
DFT_PROJECT_TYPE_NAMES = CLASSIFIERS.dft_project_type_names
_FILE_TYPE_PATTERNS = CLASSIFIERS.file_type_patterns


class CLASSIFIER_NAMES:
    """String names for built-in classifiers. Prefer CLASSIFIERS.php.name, CLASSIFIERS.names()."""

    PHP = CLASSIFIERS.php.name
    PYTHON = CLASSIFIERS.python.name
    JAVASCRIPT = CLASSIFIERS.javascript.name

    @classmethod
    def all(cls) -> List[str]:
        return CLASSIFIERS.names()

    @classmethod
    def available(cls) -> List[str]:
        return list(CLASSIFIERS.all_project_types.keys())
