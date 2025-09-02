#!/bin/bash

echo "🚀 Setting up {{ cookiecutter.project_name }} development environment..."

{% if cookiecutter.use_poetry == "yes" -%}
# Install Poetry if not already installed
if ! command -v poetry &> /dev/null; then
    echo "📦 Installing Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
    export PATH="$HOME/.local/bin:$PATH"
fi

# Install dependencies
echo "📦 Installing dependencies with Poetry..."
poetry install

echo "✅ Development environment setup complete!"
echo "🎯 Run 'poetry run uvicorn {{ cookiecutter.package_name }}.main:app --reload' to start the development server"
{% else -%}
# Install dependencies
echo "📦 Installing dependencies with pip..."
pip install -e ".[dev]"

echo "✅ Development environment setup complete!"
echo "🎯 Run 'uvicorn {{ cookiecutter.package_name }}.main:app --reload' to start the development server"
{% endif -%}