FROM python:3.8

ENV FLASK_APP app

ENV APP_NAME flask
ENV DEPENDS_DIR applications/${APP_NAME}/depends
ENV SOURCE_DIR applications/${APP_NAME}/src
ENV SCRIPTS_DIR applications/${APP_NAME}/scripts

COPY ${DEPENDS_DIR} /depends/
COPY ${SOURCE_DIR} /source/
COPY ${SCRIPTS_DIR} /scripts/

RUN apt-get update && apt-get install -y $(cat /depends/os_packages)

WORKDIR /source

RUN python3 -m venv venv
RUN . venv/bin/activate && \
    pip3 install -r /depends/requirements.txt

ENTRYPOINT ["/scripts/entrypoint.sh"]
CMD ["venv/bin/uwsgi", "--http", "0.0.0.0:8080", "--workers", "2", "--module", "app:create_app()", "--enable-threads", "--show-config"]