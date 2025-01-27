# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install core dependencies.
RUN apt-get update && apt-get install -y libpq-dev build-essential

# Upgrade pip
RUN pip install --upgrade pip setuptools wheel

# Install any Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Expose port 8000 for the Django app
EXPOSE 8000

# Run migrations and start the Django development server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
