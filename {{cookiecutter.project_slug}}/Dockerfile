FROM python:{{ cookiecutter.python_version }}-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

{% if cookiecutter.use_poetry == "yes" -%}
# Install Poetry
RUN pip install poetry==1.7.1

# Configure poetry: venvs in-project and no interaction
ENV POETRY_VENV_IN_PROJECT=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Copy poetry files
COPY pyproject.toml poetry.lock* ./

# Install dependencies
RUN poetry install --only=main && rm -rf $POETRY_CACHE_DIR

# Copy project
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["poetry", "run", "uvicorn", "{{ cookiecutter.package_name }}.main:app", "--host", "0.0.0.0", "--port", "8000"]
{% else -%}
# Copy requirements
COPY pyproject.toml ./

# Install dependencies
RUN pip install -e .

# Copy project
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "{{ cookiecutter.package_name }}.main:app", "--host", "0.0.0.0", "--port", "8000"]
{% endif -%}