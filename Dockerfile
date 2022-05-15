FROM python:3.8.0-buster
RUN apt-get update -y
RUN apt-get install -y python-pip
RUN pip install --upgrade pip
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY /app .
CMD ["python", "/app/app.py"]
