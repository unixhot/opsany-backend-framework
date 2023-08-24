# Base Image
FROM python:3.6.15-slim-bullseye

# Install PATH
RUN mkdir -p /opt/opsany/logs && mkdir /etc/supervisord.d

# Add File
ADD ./src /opt/opsany/deploy

# Install Gcc
RUN apt update -y && apt install -y build-essential libmariadb-dev && apt clean \
    && pip --no-cache-dir install supervisor gunicorn==19.9.0 gevent==1.1.2 -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com \
    && pip --no-cache-dir install -r /opt/opsany/deploy/requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

#Supervisord config
ADD supervisord.conf /etc/supervisord.conf
ADD deploy.ini /etc/supervisord.d/deploy.ini

# Outside Port
EXPOSE 7012

#supervisord start
CMD ["supervisord", "-c", "/etc/supervisord.conf"]
