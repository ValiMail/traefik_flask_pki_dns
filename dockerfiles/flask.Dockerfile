FROM alpine:3.11

ENV FLASK_APP app

ENV DOTAUTH_API_VERSION=0.4
ENV APP_NAME flask
ENV DEPENDS_DIR applications/${APP_NAME}/depends
ENV SOURCE_DIR applications/${APP_NAME}/src
ENV SCRIPTS_DIR applications/${APP_NAME}/scripts
# Because Python cryptography, that's why.
ENV CRYPTOGRAPHY_DONT_BUILD_RUST 1 

COPY ${DEPENDS_DIR} /depends/
COPY ${SOURCE_DIR} /source/
COPY ${SCRIPTS_DIR} /scripts/

RUN apk add -U $(cat /depends/os_packages)

WORKDIR /source

RUN python3 -m venv venv
RUN source venv/bin/activate && \
    pip3 install -r /depends/requirements.txt

ENTRYPOINT ["/scripts/entrypoint.sh"]
CMD ["uwsgi", "--http", "0.0.0.0:8080", "--workers", "10", "--module", "app:create_app()"]
