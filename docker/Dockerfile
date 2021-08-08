FROM python:3.9.6-buster

WORKDIR /app

COPY docker/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY server server
COPY client client
# WORKDIR ./server

EXPOSE 8000

CMD ["python", "server/manage.py", "runserver", "0.0.0.0:8000" ]
