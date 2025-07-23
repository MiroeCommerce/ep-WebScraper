# File: WebScraper/web_scraper_service/Dockerfile

# ---- Stage 1: Builder and Test Environment ----
FROM almalinux:9 AS builder

# Install Python 3.12 and build tools
RUN dnf install -y python3.12 python3.12-devel python3.12-pip gcc && dnf clean all

# Create a virtual environment
RUN python3.12 -m venv /opt/venv

# Use modern key="value" format for ENV to remove legacy format warning
ENV PATH="/opt/venv/bin:$PATH"

# Set the WORKDIR for the project root inside the container
WORKDIR /project

# Use modern key="value" format for ENV to remove legacy format warning
ENV PYTHONPATH="/project"

# Copy requirements files and pytest.ini
COPY web_scraper_service/requirements-prod.txt web_scraper_service/requirements-dev.txt ./
COPY pytest.ini ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements-prod.txt
RUN pip install --no-cache-dir -r requirements-dev.txt

# Copy the service code into a subdirectory
COPY web_scraper_service ./web_scraper_service

# Set the working directory to the service's root for running tests
WORKDIR /project/web_scraper_service

# Run only the unit tests by skipping tests marked as 'integration'
RUN python run_tests.py -m "not integration"


# ---- Stage 2: Final Production Image ----
FROM almalinux:9 AS production

# Install only the Python runtime and clean up
RUN dnf install -y python3.12 && dnf clean all

# Set the WORKDIR for the final application
WORKDIR /app

# Create a non-root user for security
RUN useradd --system --no-create-home appuser
USER appuser

# Copy the virtual environment with production dependencies from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy the entire service directory from the builder
COPY --from=builder /project/web_scraper_service ./web_scraper_service

# Use modern key="value" format for ENV to remove legacy format warning
ENV PATH="/opt/venv/bin:$PATH"

# Use modern key="value" format for ENV to remove legacy format warning
ENV PYTHONPATH="/app"

# Set the final working directory
WORKDIR /app/web_scraper_service

# Expose the application port
EXPOSE 8000

# The command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

