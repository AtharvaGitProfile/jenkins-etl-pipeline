FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY pipeline.py .
COPY data/sample/ data/sample/
RUN mkdir -p data/output
CMD ["python", "pipeline.py"]
