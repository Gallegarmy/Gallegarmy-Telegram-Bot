# Use a specific version of Python 3.12 for stability and reproducibility
FROM python:3.12-slim-bookworm

# Copy the UV binary from the external image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set the working directory to /app
WORKDIR /app

# Copy only the necessary files to install dependencies
COPY uv.lock pyproject.toml /app/

# Install the dependencies using UV, utilizing cache to speed up builds
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project

# Copy the rest of the application code after dependencies are installed
COPY . /app

# Finalize the installation of the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

# Ensure the virtual environment is used by default
ENV PATH="/app/.venv/bin:$PATH"

# Use the CMD instruction to start the application
CMD ["python", "-u","main.py"]