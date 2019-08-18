import os
import json
from embedd_face import FaceEmbedder
from celebrity_nn import CelebrityTree
import time
import logging

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


if __name__ == "__main__":
    logging.warning("starting watcher process")
    faceEmbedder = FaceEmbedder()
    celebTree = CelebrityTree()
    while True:
        try:
            process_submissions(faceEmbedder, celebTree)
            time.sleep(1)
        except Exception as e:
            logging.exception(e)
