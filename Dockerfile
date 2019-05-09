FROM python:3.7.2-alpine

ENV TZ Europe/Prague
#
RUN apk add --no-cache tzdata libstdc++ libxml2 libxml2-dev libxslt libxslt-dev && \
    apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /usr/src/daily_menu
WORKDIR /usr/src/daily_menu

ADD ./daily_menu /usr/src/daily_menu

RUN pip install --no-cache-dir -r /usr/src/daily_menu/requirements.txt

EXPOSE 8000
RUN ls -l /usr/src/daily_menu
RUN chmod +x /usr/src/daily_menu/entrypoint.sh
ENTRYPOINT /usr/src/daily_menu/entrypoint.sh

