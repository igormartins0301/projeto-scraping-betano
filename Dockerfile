FROM python:3.11.3

WORKDIR /app

COPY requirements.txt .

RUN python -m venv venv && \
    pip install -r requirements.txt

CMD ["python", "main.py"]
