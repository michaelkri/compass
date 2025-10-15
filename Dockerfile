# ====================================================================================
# Stage 1: Frontend Builder (for production)
# ====================================================================================
FROM node:22-alpine AS builder-frontend

WORKDIR /app/frontend

COPY frontend/package.json frontend/package-lock.json ./
RUN npm install --frozen-lockfile

COPY frontend/ ./
RUN npm run build


# ====================================================================================
# Stage 2: Backend Base (for development and production)
# ====================================================================================
FROM python:3.14-slim AS builder-backend

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libxml2-dev \
    libxslt-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Create and use a virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# ====================================================================================
# Stage 3: Development Stage (FOR VS CODE DEV CONTAINERS)
# ====================================================================================
FROM builder-backend AS development

# This is the target for dev containers.
# It inherits everything from builder-backend.
# VS Code will mount your local source code into /app.


# ====================================================================================
# Stage 4: Production Image (Final Stage for deployment)
# ====================================================================================
FROM builder-backend AS production

WORKDIR /app

# Copy built frontend from the first stage
COPY --from=builder-frontend /app/frontend/build /app/static

# --- START OF CHANGE ---
# Copy the contents of backend/app directly into the workdir (/app)
# This creates the correct flat structure: /app/main.py, /app/core/, etc.
COPY backend/app/ .
# --- END OF CHANGE ---

EXPOSE 8000

# --- START OF CHANGE ---
# The entrypoint is now main.py in the root of the app, not app.main
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# --- END OF CHANGE ---