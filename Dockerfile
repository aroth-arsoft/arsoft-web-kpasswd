ARG RELEASE=3-alpine
FROM python:$RELEASE

LABEL maintainer="docker@fastprotect.net"

ENV container=docker LANG=C.UTF-8

ADD ./arsoft/ /app/arsoft/
ADD ./app.py ./requirements.txt /app/

RUN apk add --update-cache krb5 && \
    pip install -r /app/requirements.txt && \
    adduser -S -s /bin/sh app

ADD ./entrypoint.sh /app/

EXPOSE 8000
CMD ["/bin/sh", "/app/entrypoint.sh"]
