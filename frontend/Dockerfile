# Use a slim Python 3.12 image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install Poetry using pip
RUN pip install poetry

# Configure Poetry to create virtualenv in the project directory
RUN poetry config virtualenvs.in-project true

# Copy Poetry files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry install --no-root 

# Copy the application files
COPY app.py ./

# Expose port 7860 for Streamlit
EXPOSE 7860

# Run the Streamlit app
CMD ["poetry", "run", "streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]