FROM python
WORKDIR /app
COPY . /app
RUN pip install flask
RUN pip install requests
RUN pip install psycopg2
CMD ["python", "ping_pong.py"]
