# Stage 1: Build Rust extension
FROM python:3.12-slim AS builder

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    g++ \
    libssl-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install Rust
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH="/root/.cargo/bin:$PATH"

# Install Maturin for building Rust extension
RUN pip install maturin

# Set working directory
WORKDIR /code

# Copy the project files
COPY ./Cargo.toml ./Cargo.lock ./pyproject.toml ./
COPY ./src ./src

# Build the Rust extension using Maturin
RUN maturin build --release --out dist

# Stage 2: Final Image
FROM python:3.12-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y libssl-dev && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /code

# Copy Python dependencies
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the built Rust extension from the builder stage
COPY --from=builder /code/dist/*.whl /code/

# Install the Rust extension as a Python package
RUN pip install /code/*.whl

# Copy the rest of the application code
COPY ./ /code/

# Expose the port
EXPOSE 8002

# Start the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]
