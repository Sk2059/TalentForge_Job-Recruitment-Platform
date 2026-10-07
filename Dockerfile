FROM python:3.11-slim

# prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1

# make python appear immediately 
ENV PYTHONUNBUFFERED 1

# working directory
WORKDIR /app

# python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
