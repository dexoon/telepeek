# Use uv Alpine image as base
FROM ghcr.io/astral-sh/uv:alpine

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install Python dependencies using uv
RUN uv sync --frozen

# Copy application code
COPY main.py ./

# Create non-root user for security
RUN adduser -D -s /bin/sh app && \
    chown -R app:app /app
USER app

# Expose port (can be overridden at runtime)
EXPOSE 80

# Run the application using uv
CMD ["uv", "run", "python", "main.py"] 