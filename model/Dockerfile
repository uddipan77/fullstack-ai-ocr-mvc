# Hugging Face Spaces: Recommended Secure Dockerfile for FastAPI

FROM python:3.10-slim

# Add a non-root user (important for HF Spaces security)
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

# Copy requirements and install as user (not root)
COPY --chown=user ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the rest of the app as user
COPY --chown=user . /app

# Expose port for FastAPI (7860 is default for Spaces)
EXPOSE 7860

# Start FastAPI app with uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]