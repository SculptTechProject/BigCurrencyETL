FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
COPY config.yaml .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
