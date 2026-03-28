# Match your local Python version 3.9.6
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    HOME=/home/user

# Create a non-root user for Hugging Face (UID 1000 is standard)
RUN useradd -m -u 1000 user
WORKDIR /code

# Copy requirements first to leverage Docker cache
COPY --chown=user requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the rest of the application
COPY --chown=user . .

# Create and set permissions for data and database folders
# This ensures ingest.py can rename processed files and Chroma can write to the DB
RUN mkdir -p /code/data /code/db/chroma_langchain_db && \
    chmod -R 777 /code/data /code/db

# Switch to the non-root user
USER user
# Expose the port for Streamlit
EXPOSE 7860

# Run the UI
# Start ingestion in the background, then start Streamlit
CMD python ingest.py & streamlit run chatbot_ui.py --server.port=7860 --server.address=0.0.0.0