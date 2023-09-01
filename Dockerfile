# Use the official Python image as a parent image
FROM python:3-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy all contents from the current directory to the container's /app directory
COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip3 install opencv-python-headless
RUN apt-get update && apt-get install libgl1-mesa-glx -y
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y

# Expose the port on which the Flask app will run
EXPOSE 5000

# Define the command to run the Flask app
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
