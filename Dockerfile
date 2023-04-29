# use official Python image
FROM python:3.10.2-slim

# Set the working directory to /app
WORKDIR /home/app

# Copy the current directory contents into the container at /app
COPY . /home/app

# Install the required Python packages
RUN pip install -r requirements.txt

# Expose the port that the app will listen on
# EXPOSE 80

# Start the FastAPI app
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]