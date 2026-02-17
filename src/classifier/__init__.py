"""
Repository Classifier Library.

Classifies GitHub repositories based on README content using a cascade
pipeline: Ground Truth → File Type Inference → Heuristic/AI methods.
"""

__version__ = '0.1.0'

from .core import (
    classify_repository_heuristic,
    classify_repository_aimodel,
)

from .registry import (
    register_classifier,
    unregister_classifier,
    get_classifier,
    get_available_classifiers,
    load_classifier_from_module,
    create_classifier_from_file,
)

from .evaluation import (
    load_ground_truth,
    save_ground_truth,
    evaluate_classifier,
    add_ground_truth_entry,
    get_ground_truth_repos,
)

from .predefine import (
    CLASSIFIER_NAMES,
    ALL_PROJECT_TYPES,
    DFT_PROJECT_TYPE_NAMES,
)

__all__ = [
    # Version
    '__version__',

    # Core classification entry points
    'classify_repository_heuristic',
    'classify_repository_aimodel',

    # Classifier registry management
    'register_classifier',
    'unregister_classifier',
    'get_classifier',
    'get_available_classifiers',
    'load_classifier_from_module',
    'create_classifier_from_file',

    # Ground truth management and evaluation
    'load_ground_truth',
    'save_ground_truth',
    'evaluate_classifier',
    'add_ground_truth_entry',
    'get_ground_truth_repos',

    # Predefined configuration constants
    'CLASSIFIER_NAMES',
    'ALL_PROJECT_TYPES',
    'DFT_PROJECT_TYPE_NAMES',
]
