# FROM ubuntu:latest
# RUN apt-get update
# RUN apt-get install -y python apache2 libapache2-mod-wsgi
# RUN apt-get install python-pip
# RUN pip install --upgrade pip
# RUN apt-get install -y git curl tar vim nano 

# I use a personal image and save on time and bandwidth
FROM bbcstar/ubuntu-python-dev
MAINTAINER Bedabrata Chatterjee

# Set up the environment
ENV APP_ENV=dev
ENV APP_PORT=80
ENV MONGO_SERVER=192.168.1.2
ENV MONGO_PORT=27017

RUN mkdir /var/www/WebInABottle 
COPY . /var/www/WebInABottle

# # Install python package dependencies
RUN pip install -r /var/www/WebInABottle/setup/requirements.txt

# Setup apache conf and enable site 
RUN cp /var/www/WebInABottle/setup/apache.conf /etc/apache2/sites-available/webinabottle.conf
RUN /usr/sbin/a2dissite 000-default
RUN /usr/sbin/a2ensite webinabottle

WORKDIR /var/www/WebInABottle

EXPOSE 80
# CMD ["/usr/sbin/apache2", "-D", "FOREGROUND"]
CMD ["/usr/sbin/service", "apache2", "start"]