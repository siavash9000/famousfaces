import uuid
from flask import request, url_for, Flask, jsonify
from flask_cors import CORS
import os
import json
import pika
import logging
import psycopg2


def create_db_structure():
    db_name = os.environ.get('DB_NAME', 'postgres')
    db_user = os.environ.get('DB_USER', 'postgres')
    db_password = os.environ.get('DB_PASSWORD', 'postgres')
    logging.info("Executing database init")
    logging.warning("Executing database init")
    connection = psycopg2.connect(dbname=db_name,
                                  user=db_user,
                                  host='postgresql',
                                  password=db_password,
                                  port=5432)
    connection.autocommit = True
    cursor = connection.cursor()
    sql = open("/facesapi/createDatabaseStructure.sql", "r").read()
    cursor.execute(sql)
    cursor.close()
    connection.close()

logging.warning("starting facesapi")
app = Flask(__name__)
CORS(app)
create_db_structure()


def queue_image(image):
    logging.debug("trying to connect to rabbitmq")
    creds = pika.PlainCredentials("ribby", "ribby")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', credentials=creds))
    channel = connection.channel()
    channel.queue_declare(queue='facecrunch_queue', durable=True)

    id_= str(uuid.uuid4())
    message = json.dumps({'image_id': id_, 'base64_image': image})
    channel.basic_publish(
        exchange='',
        routing_key='facecrunch_queue',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))
    logging.warning("Sent message {} ".format(message[0:20]))
    connection.close()
    return id_


@app.route("/face", methods=['GET', 'POST'])
def face():
    if request.method == 'POST':
        image_id = queue_image(request.json['image'])
        logging.warning("Queue id {}".format(image_id))
        return jsonify({'face_id': str(image_id)}), 201
    else:
        face_id = request.args.get('face_id')
        connection = psycopg2.connect(dbname='postgres',
                                      user='postgres',
                                      host='postgresql',
                                      password='postgres',
                                      port=5432)
        connection.autocommit = True
        cursor = connection.cursor()
        sql = "Select nearest_faces FROM face_analysis.results WHERE uuid=%s"
        cursor.execute(sql, (face_id,))
        nearest_faces = None
        if cursor.rowcount:
            nearest_faces = cursor.fetchone()[0]
        cursor.close()
        connection.close()
        if nearest_faces:
            return jsonify(nearest_faces), 200
        return jsonify({'message': 'Could not find {}'.format(face_id)}), 404


