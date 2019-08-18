# famousfaces

This repo contains the source and data of https://famousfaces.nukapi.com, an open source variant of Microsofts CelebsLikeMe. 
You take a picture of yourself and it presents you the most similar celebrities of a given set. 
You can easily add/remove faces and integrate the used react webapp into your own.

##### Table of Contents  
[Getting started](#gettingstarted)  
[Use your own images](#useyourownimages)  
[Limitations](#limitations)

<a name="gettingstarted"/>

### Getting started 


#### Install docker (skip if already installed)
https://docs.docker.com/engine/installation/

#### Clone this repo and download pretrained models:
```
git clone https://github.com/siavash9000/famousfaces.git
cd famousfaces
./download_models.sh
```

#### build and start containers
```
docker-compose build
docker-compose up
```

The application should now be available under http://localhost:3000


<a name="useyourownimages"/>

### Use your own images

You want to use your own images? Just add them to celebritydata/images, delete all files in celebritydata/embeddings.
To create new embeddings run
```
docker-compose -f build-embeddings.yml up
```
To start the application with your own images then run 
```
docker-compose up
```

<a name="limitations"/>

### Limitations:
The tensorflow version is fixed to 1.2 . Feel free to update and create a pull request! Thanks in Advance for your help!
