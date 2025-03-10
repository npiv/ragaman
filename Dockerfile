FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY pyproject.toml uv.lock ./

# Install uv
RUN pip install --no-cache-dir uv

# Install project dependencies
RUN uv pip install --system -e .

# Copy source code
COPY src/ ./src/

# Copy required files
COPY README.md ./

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["python", "-m", "ragaman.main"]