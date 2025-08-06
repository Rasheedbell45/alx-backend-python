# Use official Python 3.10 image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy all project files into container
COPY . /app/

# Expose port 8000
EXPOSE 8000

# Default command to run Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
