FROM python:3.12-slim
WORKDIR /challenge
COPY requirements.txt challenge.py output.txt ./
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "challenge.py"]
