# famousfaces
facenet + pretrained models + KDTree + WebCam = fun app

This repo contains the source and data of https://famousfaces.nukapi.com, an open source variant of Microsofts CelebsLikeMe. 
You take a picture of yourself and it presents you the most similar celebrities of a given set. 
You can easily add/reove faces and integrate the used react webapp into your own.

### Limitations:

The tensorflow version is fixed to 1.2 . Feel free to update and create a pull request! Thanks in Advance for your help!

### Getting started:

#### Install docker (skip if already installed)
https://docs.docker.com/engine/installation/

#### Clone this repo and download pretrained models:
```
git clone https://github.com/siavash9000/famousfaces.git
cd famousfaces
./download_models.sh
```

#### build docker images
```
cd famousfaces
docker-compose build
```

##### start containers
```
docker-compose up
```

The application should now be available under http://localhost:3000
