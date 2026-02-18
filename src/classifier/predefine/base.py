"""
Abstract base class for language-specific classifier configuration.

Subclass and implement the abstract properties (name, project_types, file_patterns).
Extend by adding a new module with a concrete subclass and a singleton instance.
"""

from abc import ABC, abstractmethod
from typing import Dict, List


class LanguageClassifier(ABC):
    """Abstract interface for one language classifier.

    Subclasses must implement: name, project_types, file_patterns.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Language identifier (e.g. 'php', 'python', 'javascript')."""
        ...

    @property
    @abstractmethod
    def project_types(self) -> Dict[str, Dict[str, int]]:
        """Map project type name -> keyword -> weight for heuristic classification."""
        ...

    @property
    @abstractmethod
    def file_patterns(self) -> Dict[str, List[str]]:
        """Map project type name -> list of file/path patterns for file-type inference."""
        ...

    @property
    def project_type_names(self) -> List[str]:
        """Ordered list of project type names (keys of project_types)."""
        return list(self.project_types.keys())
