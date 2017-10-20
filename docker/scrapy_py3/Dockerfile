FROM alpine:latest
MAINTAINER <cajan2>
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories

RUN apk -U add  \
        gcc \
        libffi-dev \
        libxml2-dev \
        libxslt-dev \
        musl-dev \
        openssl-dev \
        curl ca-certificates \
        python3 && \
    python3 -m ensurepip && \
    && curl ca-certificates \
    && update-ca-certificates \
    && rm -rf /var/cache/apk/* \

RUN mkdir -p /runtime/app
WORKDIR /runtime/app
COPY requirements.txt /runtime/app
RUN  pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com



