FROM ubuntu:latest

VOLUME ["/app"]

# Update package list and install Flask And Bind9 + Supervisor
RUN apt-get update \
    && apt-get install -y bind9 bind9utils bind9-doc net-tools dnsutils \
    python3 python3-pip supervisor

# Create directory and set permissions for Bind9 logs
RUN mkdir /var/named/ \
    && mkdir /var/named/log

# Set the working directory for Flask
WORKDIR /app

## install the dependencies and packages in the requirements file for the flask app
COPY ./app/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Copy supervisor configuration file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

#5000 for flask, the 53 for dns and 953 for reverse dns
EXPOSE 53/tcp
EXPOSE 53/udp
EXPOSE 953/tcp
EXPOSE 5000

CMD ["/usr/bin/supervisord"]