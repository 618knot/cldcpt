FROM python:3.12.0
WORKDIR /app

COPY ./requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --no-cache-dir uvicorn[standard]