# base image
FROM docker/whalesay:latest

# install fortunes into this image
RUN apt-get -y update 
RUN apt-get install -y fortunes

# run fortunes and pipe into cowsay
CMD /usr/games/fortune -a | cowsay
