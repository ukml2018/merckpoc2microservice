# Use a base image with Python pre-installed
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

RUN pip install --upgrade pip
#RUN pip install --upgrade ibm-generative-ai
# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade ibm-generative-ai
# Copy the application code to the working directory
COPY . .

# Expose the port on which the Flask application will run (default is 5000)
EXPOSE 5000

# Set the environment variable for Flask
ENV FLASK_APP=application.py

# Run the Flask application
CMD ["flask", "run", "--host=0.0.0.0"]
