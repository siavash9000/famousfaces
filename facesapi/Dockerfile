FROM continuumio/miniconda3
RUN pip install flask flask-cors gunicorn pika==1.1.0
WORKDIR /facesapi
ADD . /facesapi
EXPOSE 8081
CMD gunicorn --workers=4 --bind=0.0.0.0:8081 api:app