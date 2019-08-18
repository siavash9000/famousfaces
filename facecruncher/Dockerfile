FROM tensorflow/tensorflow:1.2.0
RUN apt update && apt install -y libsm6 libxext6 libxrender-dev
WORKDIR /facecruncher
ADD . /facecruncher
ADD requirements.txt /facecruncher/requirements.txt
RUN python -m pip install -r requirements.txt
CMD python /facecruncher/src/watcher.py