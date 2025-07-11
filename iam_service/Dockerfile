FROM python:3.10-slim
WORKDIR /app

# Copy requirements and install
COPY iam_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development
ENV PYTHONPATH=/app

EXPOSE 5000

CMD ["flask", "run"]