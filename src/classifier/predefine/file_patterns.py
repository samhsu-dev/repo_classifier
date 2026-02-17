"""
File-type pattern definitions for cascade classification.

Maps classifier names to project-type file patterns. Patterns are plain
strings matched case-insensitively against tokens extracted from README.
"""

from typing import Dict, List

# PHP project types and their characteristic file patterns
_PHP_PATTERNS: Dict[str, List[str]] = {
    "Web App": [
        "index.php", "public/index.php", ".htaccess",
        "wp-config.php", "config.php", "routes/web.php",
    ],
    "Framework": [
        "artisan", "composer.json", "symfony.lock",
        "config/app.php", "bootstrap/app.php",
    ],
    "Framework Plugin": [
        "plugin.php", "wp-content/plugins",
        "modules/", "drupal.info",
    ],
    "Framework Theme": [
        "style.css", "functions.php", "theme.json",
        "templates/", "wp-content/themes",
    ],
    "Library": [
        "composer.json", "src/", "vendor/",
        "phpunit.xml", "phpstan.neon",
    ],
    "CLI App": [
        "bin/console", "bin/cli", "symfony/console",
    ],
    "PHP-SRC": [
        "zend_vm_execute.h", "ext/", "sapi/",
        "zend_api.h", "php-src",
    ],
}

# Python project types and their characteristic file patterns
_PYTHON_PATTERNS: Dict[str, List[str]] = {
    "Web Framework": [
        "manage.py", "wsgi.py", "asgi.py",
        "app.py", "settings.py", "urls.py",
        "requirements.txt", "pyproject.toml",
    ],
    "Data Science": [
        ".ipynb", "notebook", "requirements.txt",
        "environment.yml", "data/", "models/",
    ],
    "CLI Tool": [
        "setup.cfg", "entry_points", "console_scripts",
        "__main__.py", "cli.py",
    ],
    "Library/Package": [
        "setup.py", "pyproject.toml", "setup.cfg",
        "src/", "__init__.py", "tox.ini",
    ],
    "Web Scraping": [
        "scrapy.cfg", "spiders/", "items.py",
        "pipelines.py", "middlewares.py",
    ],
    "API/Backend": [
        "app.py", "main.py", "routers/",
        "endpoints/", "schemas/", "openapi",
    ],
    "Desktop Application": [
        "ui/", "gui/", "mainwindow",
        ".ui", ".qrc", "resources/",
    ],
    "Testing Tool": [
        "conftest.py", "pytest.ini", "tox.ini",
        "tests/", "test_", "noxfile.py",
    ],
}

# JavaScript project types and their characteristic file patterns
_JAVASCRIPT_PATTERNS: Dict[str, List[str]] = {
    "Frontend Framework": [
        "package.json", "src/app", "src/index",
        ".jsx", ".tsx", "public/index.html",
        "vite.config", "next.config",
    ],
    "Node.js Backend": [
        "server.js", "app.js", "index.js",
        "package.json", "routes/", "controllers/",
        "middleware/", "express",
    ],
    "Static Site Generator": [
        "gatsby-config", "next.config", "nuxt.config",
        "content/", "posts/", "_config.yml",
    ],
    "JavaScript Library": [
        "package.json", "rollup.config", "tsconfig.json",
        "dist/", "lib/", "src/index",
    ],
    "UI Component Library": [
        "storybook", ".storybook/", "components/",
        "styles/", "theme/", "tokens/",
    ],
    "Mobile App Framework": [
        "app.json", "metro.config", "ios/",
        "android/", "capacitor.config",
    ],
    "Build Tool": [
        "webpack.config", "rollup.config", "esbuild",
        "vite.config", "tsconfig.json", "babel.config",
    ],
    "Testing Framework": [
        "jest.config", "cypress.config", "mocha",
        ".nycrc", "karma.conf", "playwright.config",
    ],
}

# Global unified file pattern registry (internal use only)
_FILE_TYPE_PATTERNS: Dict[str, Dict[str, List[str]]] = {
    "php": _PHP_PATTERNS,
    "python": _PYTHON_PATTERNS,
    "javascript": _JAVASCRIPT_PATTERNS,
}
