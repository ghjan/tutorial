FROM alpine:latest
MAINTAINER <cajan2>
RUN apk -U add \
        gcc \
        libffi-dev \
        libxml2-dev \
        libxslt-dev \
        musl-dev \
        openssl-dev \
        python-dev \
        py-imaging \
        py-pip \
        curl ca-certificates \
    && update-ca-certificates \
    && rm -rf /var/cache/apk/* \
    && pip install --upgrade pip \

COPY ./requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /runtime/app
