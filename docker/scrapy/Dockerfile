FROM alpine:latest
MAINTAINER <cajan2>
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories
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
    && pip install --upgrade pip
    
RUN mkdir -p /runtime/app
WORKDIR /runtime/app
COPY requirements.txt /runtime/app
RUN  pip install -r requirements.txt



