import uuid
from flask import request, url_for, Flask, jsonify
from flask_cors import CORS
from os import path
import base64
import json


app = Flask(__name__)
CORS(app)

def persist_image(image):
    image_id = uuid.uuid4()
    filename = str(image_id) + '.jpeg'
    with open(path.join("/submissions", filename), "wb") as f:
        f.write(base64.b64decode(image))
    return image_id


@app.route("/facesapi/face", methods=['GET', 'POST'])
def face():
    if request.method == 'POST':
        image_id = persist_image(request.json['image'])
        return jsonify({'face_id': str(image_id)}), 201
    else:
        face_id = request.args.get('face_id')
        submission_filename = path.join("/submissions", str(face_id) + '.jpeg')
        if path.isfile(submission_filename):
            return jsonify({}), 202
        result_filename = path.join("/results", str(face_id) + '.json')
        if path.isfile(result_filename):
            with open(result_filename, "r") as f:
                result = json.loads(f.read())
            return jsonify(result), 200
        return jsonify({'message': 'Could not find {}'.format(result_filename)}), 404

