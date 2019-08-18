import numpy
import os
from scipy.spatial import KDTree
import urllib
import logging
import os

CELEBRITY_DATA_URL = os.environ.get('CELEBRITY_DATA_URL','https://celebritydata.nukapi.com')

IMAGE_BASE_URL = CELEBRITY_DATA_URL + "/images/"
EMBEDDINGS_URL = CELEBRITY_DATA_URL + "/embeddings/embeddings.npy"
IMAGELIST_URL = CELEBRITY_DATA_URL + "/embeddings/image_list.npy"


class CelebrityTree(object):
    def __init__(self, embeddings_path='./embeddings.npy', imagelist_path='./image_list.npy'):
        logging.warning('EMBEDDINGS_URL: {}'.format(EMBEDDINGS_URL))
        urllib.urlretrieve(EMBEDDINGS_URL, './embeddings.npy')
        logging.warning('IMAGELIST_URL: {}'.format(IMAGELIST_URL))
        urllib.urlretrieve(IMAGELIST_URL, './image_list.npy')
        embeddings = numpy.load(embeddings_path)
        image_list = numpy.load(imagelist_path)
        self.cleaned_imagelist = list(map(lambda x: x.split('/')[-2]+'/' + x.split('/')[-1], image_list))
        self.tree = KDTree(embeddings)

    def nearest_celeb_faces(self, face_embedding, nn_count):
        celebs = list(map(lambda x: self.cleaned_imagelist[x], self.tree.query(face_embedding, nn_count)[1]))
        dists = list(self.tree.query(face_embedding, nn_count)[0])
        return zip(celebs, dists)

    def face_analysis(self, face_embedding):
        celeb_dists = self.nearest_celeb_faces(face_embedding, 20)
        grouped = {}
        for celeb in celeb_dists:
            name = celeb[0].split('/')[0]
            if name not in grouped:
                grouped[name] = []
            grouped[name].append(celeb)
        counts = {}
        for name in grouped.iterkeys():
            dists = list(map(lambda x: x[1], grouped[name]))
            counts[name] = min(dists)
        sorted_counts = sorted(counts.items(), key=lambda x: x[1])
        top_counts = sorted_counts[0:3]
        result = {}
        for top in top_counts:
            entries = grouped[top[0]]
            extended_entries = []
            for entry in entries:
                extended_entries.append(IMAGE_BASE_URL + entry[0])
            result[top[0]] = extended_entries
        return result

