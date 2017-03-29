# Docker Setup

# Build the image for the WFE 
$ docker build -f wfe.dockerfile   -t bbcstar/webinabottle-wfe .

# Build the infrastructure using docker-compose
$ docker-compose build

# Bring up the services
$ docker-compose up


# Once done, tear up the services
$ docker-compose down


