FROM python:3-slim
COPY . /app
WORKDIR /app
RUN python3 -m ensurepip && python3 -m pip install -r requirements.txt
CMD ["python3", "main.py"]
