# Use a lightweight base image
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Create a directory for debugging
RUN mkdir /app/debug

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install chromium for playwright
RUN playwright install-deps
RUN playwright install chromium

# Copy the rest of the application code
COPY . .

# Make the start script executable
RUN chmod +x start.sh

# Expose the port the app runs on
EXPOSE 5000

CMD ["bash", "./start.sh"]