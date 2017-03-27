# Dockerfile for WebInABottle

# Get an Ubuntu image and install basic packages
FROM ubuntu:latest
RUN apt-get update
RUN apt-get install -y python-pip && apt-get install -y git
RUN pip install --upgrade pip

# Install MongoDB and setup the database directory
RUN apt-get install -y mongodb-org
RUN mkdir -p /data/db
RUN mkdir -p /var/log/mongo
# Expose port 27017 from the container to the host
EXPOSE 27017
RUN mongod --fork --dbpath /data/db --logpath /var/log/mongo/mongodb.log

# Set up the application
WORKDIR /var/www
RUN git clone https://github.com/bbcCorp/WebInABottle.git
WORKDIR /var/www/WebInABottle
RUN pip install -r ./setup/requirements.txt
CMD python ./setup/authSetup.py

# Run the application and expose the port
CMD ./web/run.sh
EXPOSE 1337
