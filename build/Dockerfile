FROM python:3.8-slim

RUN useradd admin

# package cloudstorage bug for storing files to local
RUN apt-get update && apt-get install -y libmagic1

WORKDIR /home/admin
RUN chown -R admin:admin ./

COPY requirements.txt requirements.txt
RUN python3 -m venv venv
RUN venv/bin/pip3 install -r requirements.txt

# minimum image size, copy and chown
COPY --chown=admin:admin pshouse_schedule pshouse_schedule
COPY --chown=admin:admin tests tests
COPY --chown=admin:admin app.py boot.sh requirements.test.txt ./

RUN chmod +x boot.sh

USER admin
