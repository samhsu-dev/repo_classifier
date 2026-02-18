"""
PHP project type configuration.

Implements LanguageClassifier for PHP: project types, keyword weights, file patterns.
"""

from .base import LanguageClassifier


class PHPClassifier(LanguageClassifier):
    """PHP language classifier. Implement abstract interface."""

    name = "php"

    file_patterns = {
        "Web App": [
            "index.php",
            "public/index.php",
            ".htaccess",
            "wp-config.php",
            "config.php",
            "routes/web.php",
        ],
        "Framework": [
            "artisan",
            "composer.json",
            "symfony.lock",
            "config/app.php",
            "bootstrap/app.php",
        ],
        "Framework Plugin": [
            "plugin.php",
            "wp-content/plugins",
            "modules/",
            "drupal.info",
        ],
        "Framework Theme": [
            "style.css",
            "functions.php",
            "theme.json",
            "templates/",
            "wp-content/themes",
        ],
        "Library": [
            "composer.json",
            "src/",
            "vendor/",
            "phpunit.xml",
            "phpstan.neon",
        ],
        "CLI App": [
            "bin/",
            "console",
            "artisan",
        ],
        "PHP-SRC": [
            "Zend/",
            "php-src",
            "main/php.h",
        ],
    }

    project_types = {
        "Web App": {
            "web application": 10,
            "web app": 10,
            "webapp": 8,
            "cms": 8,
            "content management": 8,
            "ecommerce": 8,
            "e-commerce": 8,
            "online store": 8,
            "blog": 5,
            "website": 5,
        },
        "Framework": {
            "framework": 10,
            "mvc": 8,
            "model-view-controller": 8,
            "application framework": 10,
            "web framework": 10,
        },
        "Framework Plugin": {
            "plugin": 10,
            "extension": 8,
            "addon": 8,
            "add-on": 8,
            "module": 5,
            "wordpress plugin": 10,
            "drupal module": 10,
            "joomla extension": 10,
        },
        "Framework Theme": {
            "theme": 10,
            "template": 8,
            "skin": 5,
            "wordpress theme": 10,
            "drupal theme": 10,
            "joomla template": 10,
        },
        "Library": {
            "library": 10,
            "package": 8,
            "component": 5,
            "helper": 5,
            "utility": 5,
            "composer": 8,
        },
        "CLI App": {
            "cli": 10,
            "command line": 10,
            "console": 8,
            "terminal": 8,
            "shell": 5,
        },
        "PHP-SRC": {
            "php-src": 15,
            "php source": 15,
            "php interpreter": 15,
            "php language": 15,
            "php core": 15,
            "zend engine": 15,
        },
    }


PHP = PHPClassifier()
