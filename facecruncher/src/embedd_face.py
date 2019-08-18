from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import time
from scipy import misc
import tensorflow as tf
import numpy as np
import sys
import os
import argparse
import facenet
import align.detect_face
import glob
from six.moves import xrange
import logging


class FaceEmbedder(object):
    def __init__(self, model_dir="/facecruncher/src/pretrained_models", gpu_memory_fraction=1.0):
        self.face_graph = tf.Graph()
        start_time = time.time()
        with self.face_graph.as_default():
            self.face_session = tf.Session()
            with self.face_session.as_default():
                facenet.load_model(model_dir)
        logging.warning("loading facenet model took {}".format(time.time() - start_time))

        self.minsize = 20 # minimum size of face
        self.threshold = [ 0.6, 0.7, 0.7 ]  # three steps's threshold
        self.factor = 0.709 # scale factor
        start_time = time.time()
        with tf.Graph().as_default():
            gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=gpu_memory_fraction)
            sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
            with sess.as_default():
                self.pnet, self.rnet, self.onet = align.detect_face.create_mtcnn(sess, None)
        logging.warning("loading face allignement model took{}".format(time.time() - start_time))

    def embedd_face(self, image_path, image_size=160, margin=44,
                    is_aligned=False, gpu_memory_fraction=1.0):
        with self.face_graph.as_default():
            with self.face_session.as_default():
                start_time = time.time()
                images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
                embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
                phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
                if is_aligned is True:
                    images = facenet.load_data(image_path, False, False, image_size)
                else:
                    images = self.load_and_align_data(image_path, image_size, margin)
                feed_dict = { images_placeholder: images, phase_train_placeholder:False }
                embed = self.face_session.run(embeddings, feed_dict=feed_dict)
                logging.warning("complete runtime {}".format(time.time() - start_time))
                return embed[0]

    def load_and_align_data(self, image_path, image_size, margin):
        img = misc.imread(os.path.expanduser(image_path))
        img_size = np.asarray(img.shape)[0:2]
        try:
            bounding_boxes, _ = align.detect_face.detect_face(img, self.minsize, self.pnet, self.rnet,
                                                              self.onet, self.threshold, self.factor)
        except:
            logging.warning('Could not detect face in image.')
            bounding_boxes = None
        if bounding_boxes is not None and bounding_boxes.size:
            det = np.squeeze(bounding_boxes[0,0:4])
            bb = np.zeros(4, dtype=np.int32)
            bb[0] = np.maximum(det[0]-margin/2, 0)
            bb[1] = np.maximum(det[1]-margin/2, 0)
            bb[2] = np.minimum(det[2]+margin/2, img_size[1])
            bb[3] = np.minimum(det[3]+margin/2, img_size[0])
            cropped = img[bb[1]:bb[3],bb[0]:bb[2],:]
            aligned = misc.imresize(cropped, (image_size, image_size), interp='bilinear')
            prewhitened = facenet.prewhiten(aligned)
            images = np.stack([prewhitened])
        else:
            images = np.stack([np.zeros((160, 160, 3))])
        return images
