FROM --platform=linux/amd64 python:3.9 as build

WORKDIR /app

COPY . /app

RUN pip install flask
RUN pip install requests


EXPOSE 5000

CMD ["python", "todoer.py"]