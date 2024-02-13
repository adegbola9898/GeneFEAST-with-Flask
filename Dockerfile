# Start with the GeneFEAST Docker image as the base
FROM ghcr.io/avigailtaylor/genefeast:latest

# Install Flask and Gunicorn in the Docker image
RUN pip install Flask gunicorn

# Copy the Flask application script and other files to the Docker image
COPY . /app

# Change the working directory to /app
WORKDIR /app

# Install any additional dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define environment variable for Google Cloud Storage bucket name
ENV GCS_BUCKET_NAME=samyus2

# Run app.py using Gunicorn when the container launches
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
