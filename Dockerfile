# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV FLASK_APP=app
ENV FLASK_ENV=development
ENV FLASK_DEBUG=true
ENV FLASK_RUN_PORT=3000

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Expose the port the app runs on
EXPOSE 3000

# Run Flask when the container launches
CMD ["flask", "run", "--host=0.0.0.0", "--port=3000"]
