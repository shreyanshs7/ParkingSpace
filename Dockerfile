FROM python:2.7-slim

#================================================================
# add dependencies
#================================================================

RUN apk add --update --no-cache \
    g++ gcc postgresql-dev libffi-dev tzdata

RUN cp /usr/share/zoneinfo/UTC /etc/localtime
ENV TZ UTC

#================================================================
# pip and required modules install
#================================================================

### Upgrade pip to prevent errors
RUN pip install setuptools --upgrade
ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

#================================================================
# source code copy and setup
#================================================================
RUN mkdir -p /parking-space
WORKDIR /parking-space
ADD . /parking-space

#================================================================
# expose the correct port and run
#================================================================
EXPOSE 9000
ENTRYPOINT /bin/ash run.sh