FROM alpine:3.12.0

LABEL Description="Small Flask app for getting some inspiration from deep quotes and cozy pictures"
LABEL Maintainer="nikonov.andrew@gmail.com"

COPY . /app

WORKDIR /app

RUN apk add --no-cache git python3 ca-certificates libffi-dev && \
    apk add --no-cache --virtual=build-dependencies build-base linux-headers python3-dev && \
    apk add --no-cache py3-pip && \
    pip3 install --no-cache-dir -r requirements.txt && \
    apk del build-dependencies && \
    rm -rf /tmp/* /var/tmp/* /var/cache/apk/*

EXPOSE 42069/tcp

RUN python3 createdb.py

CMD ["python3", "flask_app.py"]
