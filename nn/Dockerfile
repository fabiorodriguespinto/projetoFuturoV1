FROM python:3.11-slim
WORKDIR /app
COPY ./training /app
RUN pip install --no-cache-dir scikit-learn pandas numpy
CMD ["python", "train.py"]
