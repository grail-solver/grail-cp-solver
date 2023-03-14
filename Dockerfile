FROM python:latest

WORKDIR /app
COPY requirements.txt ./
COPY main.py ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY ./app /app/app
EXPOSE 8000
