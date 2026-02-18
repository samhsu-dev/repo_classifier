"""
JavaScript project type configuration.

Implements LanguageClassifier for JavaScript: project types, keyword weights, file patterns.
"""

from .base import LanguageClassifier


class JavaScriptClassifier(LanguageClassifier):
    """JavaScript language classifier. Implement abstract interface."""

    name = "javascript"

    file_patterns = {
        "Frontend Framework": [
            "package.json",
            "src/App.js",
            "src/App.jsx",
            "src/App.tsx",
            "vite.config",
            "next.config",
            "nuxt.config",
        ],
        "Node.js Backend": [
            "package.json",
            "index.js",
            "server.js",
            "app.js",
            "express",
            "koa",
        ],
        "Static Site Generator": [
            "package.json",
            "gatsby-config",
            "next.config",
            "nuxt.config",
            "config.toml",
        ],
        "JavaScript Library": [
            "package.json",
            "src/",
            "lib/",
            "dist/",
            "rollup.config",
            "webpack.config",
        ],
        "UI Component Library": [
            "package.json",
            "components/",
            "src/",
            "storybook",
            "*.stories.",
        ],
        "Mobile App Framework": [
            "app.json",
            "metro.config",
            "ios/",
            "android/",
            "capacitor.config",
        ],
        "Build Tool": [
            "webpack.config",
            "rollup.config",
            "esbuild",
            "vite.config",
            "tsconfig.json",
            "babel.config",
        ],
        "Testing Framework": [
            "jest.config",
            "cypress.config",
            "mocha",
            ".nycrc",
            "karma.conf",
            "playwright.config",
        ],
    }

    project_types = {
        "Frontend Framework": {
            "react": 10,
            "vue": 10,
            "angular": 10,
            "svelte": 10,
            "frontend": 8,
            "ui framework": 8,
            "component": 5,
            "jsx": 8,
            "tsx": 8,
            "spa": 8,
            "single page application": 8,
        },
        "Node.js Backend": {
            "node.js": 10,
            "nodejs": 10,
            "express": 10,
            "koa": 10,
            "fastify": 10,
            "nest.js": 10,
            "nestjs": 10,
            "backend": 8,
            "server": 8,
            "api": 5,
            "rest": 5,
            "graphql": 5,
        },
        "Static Site Generator": {
            "static site": 10,
            "gatsby": 10,
            "next.js": 10,
            "nextjs": 10,
            "nuxt": 10,
            "jekyll": 10,
            "hugo": 10,
            "ssg": 10,
            "jamstack": 8,
            "static website": 8,
        },
        "JavaScript Library": {
            "library": 10,
            "utility": 8,
            "helper": 8,
            "toolkit": 8,
            "npm package": 10,
            "npm module": 10,
            "javascript library": 10,
            "js library": 10,
        },
        "UI Component Library": {
            "ui component": 10,
            "component library": 10,
            "ui kit": 10,
            "design system": 10,
            "material-ui": 8,
            "bootstrap": 8,
            "tailwind": 8,
            "chakra": 8,
            "styled-components": 8,
        },
        "Mobile App Framework": {
            "react native": 10,
            "reactnative": 10,
            "ionic": 10,
            "cordova": 10,
            "capacitor": 10,
            "mobile app": 10,
            "mobile framework": 10,
            "cross-platform": 8,
            "hybrid app": 8,
        },
        "Build Tool": {
            "webpack": 10,
            "rollup": 10,
            "parcel": 10,
            "esbuild": 10,
            "vite": 10,
            "bundler": 10,
            "build tool": 10,
            "module bundler": 10,
            "transpiler": 8,
            "babel": 8,
        },
        "Testing Framework": {
            "jest": 10,
            "mocha": 10,
            "chai": 10,
            "jasmine": 10,
            "cypress": 10,
            "testing": 10,
            "test framework": 10,
            "unit test": 8,
            "e2e test": 8,
            "integration test": 8,
        },
    }


JAVASCRIPT = JavaScriptClassifier()
