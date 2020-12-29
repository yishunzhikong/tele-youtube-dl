# base image
FROM lsiobase/alpine.python3:latest as builder

# MAINTAINER
MAINTAINER yishunzhikong@163.com

ADD ./ /root/
VOLUME ["/downloads","/root/conf"]

RUN pip install --upgrade pip
RUN pip install python-telegram-bot --upgrade
RUN pip install --upgrade youtube-dl
RUN apk add ffmpeg

ENTRYPOINT ["/bin/bash","/root/setup.sh"]