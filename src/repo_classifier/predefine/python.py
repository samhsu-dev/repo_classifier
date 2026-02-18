"""
Python project type configuration.

Implements LanguageClassifier for Python: project types, keyword weights, file patterns.
"""

from .base import LanguageClassifier


class PythonClassifier(LanguageClassifier):
    """Python language classifier. Implement abstract interface."""

    name = "python"

    # Only files that imply the project *is* this type (not just "uses" the tool). E.g. pytest.ini = uses testing ≠ is Testing Tool.
    file_patterns = {
        "Web Framework": [],  # No file that implies project is a web framework
        "Data Science": [],  # environment.yml/.ipynb = uses conda/notebooks, not necessarily a DS project
        "CLI Tool": [],
        "Library/Package": [],
        "Web Scraping": [
            "scrapy.cfg",  # Scrapy project ⇒ project is a scraping/crawler project
        ],
        "API/Backend": [],  # openapi/swagger = documents API, not necessarily "is API backend project"
        "Desktop Application": [],
        "Testing Tool": [],  # pytest/tox/coveragerc = uses testing tools, not "is a testing tool project"
    }

    project_types = {
        "Web Framework": {
            "django": 10,
            "flask": 10,
            "fastapi": 10,
            "web framework": 8,
            "wsgi": 5,
            "asgi": 5,
            "pyramid": 8,
            "tornado": 8,
            "bottle": 8,
            "web server": 5,
        },
        "Data Science": {
            "data science": 10,
            "machine learning": 10,
            "deep learning": 10,
            "numpy": 8,
            "pandas": 8,
            "scikit-learn": 8,
            "tensorflow": 8,
            "pytorch": 8,
            "keras": 8,
            "jupyter": 7,
            "notebook": 5,
            "data analysis": 8,
            "data visualization": 8,
            "matplotlib": 7,
            "seaborn": 7,
        },
        "CLI Tool": {
            "command line": 10,
            "cli": 10,
            "terminal": 8,
            "console": 8,
            "argparse": 5,
            "click": 5,
            "typer": 5,
            "shell": 5,
            "command-line": 10,
            "commandline": 10,
        },
        "Library/Package": {
            "library": 10,
            "package": 10,
            "module": 8,
            "pip": 5,
            "pypi": 5,
            "dependency": 5,
            "helper": 5,
            "utility": 5,
            "toolkit": 8,
        },
        "Web Scraping": {
            "scraping": 10,
            "crawler": 10,
            "spider": 10,
            "beautifulsoup": 8,
            "requests": 5,
            "selenium": 5,
            "web scraper": 10,
            "html parser": 8,
            "data extraction": 8,
        },
        "API/Backend": {
            "api": 10,
            "rest": 10,
            "restful": 10,
            "graphql": 10,
            "backend": 10,
            "microservice": 8,
            "server": 5,
            "endpoint": 8,
            "http": 5,
            "json": 5,
        },
        "Desktop Application": {
            "desktop": 10,
            "gui": 10,
            "tkinter": 8,
            "pyqt": 8,
            "pyside": 8,
            "wxpython": 8,
            "kivy": 8,
            "qt": 7,
            "user interface": 5,
            "desktop app": 10,
        },
        "Testing Tool": {
            "testing": 10,
            "test": 8,
            "pytest": 10,
            "unittest": 10,
            "mock": 8,
            "assertion": 5,
            "test suite": 8,
            "test case": 8,
            "test runner": 8,
        },
    }


PYTHON = PythonClassifier()
