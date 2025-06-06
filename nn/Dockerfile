# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app/nn

# Copy the requirements file into the container at /app/nn
# Note: main.py is in the nn directory, so uvicorn will run main:app from /app/nn
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app/nn
# This includes main.py and the modelos directory (which should be created by the training process or mounted)
COPY . .

# Make port 8001 available to the world outside this container
EXPOSE 8001

# Define environment variable
ENV PYTHONUNBUFFERED 1

# Run main.py when the container launches
# The command should refer to main:app because main.py is in the WORKDIR /app/nn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
