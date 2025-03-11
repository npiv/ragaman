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
COPY docs/ ./docs/

# Expose ports
EXPOSE 8000  # API port
EXPOSE 8080  # MCP HTTP port

# Command will be overridden in docker-compose.yml
CMD ["python", "-m", "ragaman.main"]