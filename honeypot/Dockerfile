# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy honeypot modules
COPY core/ /app/core/
COPY services/ /app/services/
COPY detection/ /app/detection/
COPY responses/ /app/responses/
COPY config.py /app/
COPY profiles.json /app/
COPY main.py /app/

# Create logs directory and set permissions
RUN mkdir -p /logs && \
    useradd -m honeypotuser && \
    chown -R honeypotuser:honeypotuser /logs
USER honeypotuser

# Expose the ports
EXPOSE 8080 2222

# Run honeypot
CMD ["python", "-u", "main.py"]
