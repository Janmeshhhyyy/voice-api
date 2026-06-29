# 1. Start with a lightweight Linux + Python 3.10 environment
FROM python:3.10-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy our requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy our server code into the container
COPY main.py .

# 5. Tell the container which port to expose
EXPOSE 8000

# 6. The command that runs when the container starts
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]