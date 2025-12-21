# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Set working directory
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy dependency files first
COPY pyproject.toml .
COPY uv.lock .

# Install dependencies
# --no-dev: valid for production
# --no-editable: redundant but safe
# --system: install into system python (env is simpler in docker)
RUN uv sync --frozen --no-dev --no-editable

# Copy the application code
COPY . .

# Expose port
EXPOSE 8000

# Command to run the application
# Use shell form to allow variable expansion if needed, but array form is safer
CMD ["/app/.venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
