import os
import json
from embedd_face import FaceEmbedder
from celebrity_nn import CelebrityTree
import psycopg2
import logging
import pika
import base64


submissions_folder = '/submissions/'
results_folder = '/results/'


def sorted_dir(folder):
    def getmtime(name):
        path = os.path.join(folder, name)
        return os.path.getmtime(path)
    files = os.listdir(folder)
    filtered = []
    for f in files:
        if f.endswith(".jpg") or f.endswith(".jpeg"):
            filtered.append(f)
    return sorted(filtered, key=getmtime, reverse=False)


def process_submissions(faceEmbedder, celebrityTree):
    files = sorted_dir(submissions_folder)
    for file in files:
        file_path = os.path.join(submissions_folder, file)
        embedding = faceEmbedder.embedd_face(file_path)
        result = celebrityTree.face_analysis(embedding)
        result_filename = file.split('.')[0] + '.json'
        with open(os.path.join(results_folder, result_filename), 'w') as fp:
            json.dump(result, fp)
        os.remove(file_path)


class Cruncher(object):
    def __init__(self, faceEmbedder, celebTree):
        self.faceEmbedder = faceEmbedder
        self.celebTree = celebTree

    def process_message(self, ch, method, properties, body):
        body_json = json.loads(body)
        image = body_json['base64_image']
        image = base64.b64decode(image)
        embedding = faceEmbedder.embedd_face(image)
        result = self.celebTree.face_analysis(embedding)
        connection = psycopg2.connect(dbname='postgres',
                                      user='postgres',
                                      host='postgresql',
                                      password='postgres',
                                      port=5432)
        connection.autocommit = True
        cursor = connection.cursor()
        sql = "INSERT INTO face_analysis.results (uuid, nearest_faces) VALUES(%s, %s)"
        cursor.execute(sql, (body_json['image_id'], json.dumps(result)))
        cursor.close()
        connection.close()
        ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == "__main__":
    logging.warning("starting watcher process")
    faceEmbedder = FaceEmbedder()
    celebTree = CelebrityTree()
    cruncher = Cruncher(faceEmbedder=faceEmbedder, celebTree=celebTree)
    creds = pika.PlainCredentials("ribby", "ribby")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', credentials=creds))
    channel = connection.channel()
    channel.queue_declare(queue='facecrunch_queue', durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='facecrunch_queue', on_message_callback=cruncher.process_message)

    channel.start_consuming()
