FROM tensorflow/tensorflow:1.2.0
RUN apt update && apt install -y libsm6 libxext6 libxrender-dev libpq-dev
WORKDIR /facecruncher
ADD requirements.txt /facecruncher/requirements.txt
RUN python -m pip install -r requirements.txt
ADD . /facecruncher
RUN cd src/pretrained_models/ && cat x* > model.zip && unzip model.zip && cd /facecruncher
CMD python /facecruncher/src/watcher.py