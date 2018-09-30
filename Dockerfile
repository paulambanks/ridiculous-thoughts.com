FROM python:3.7.0-alpine3.8 as build
RUN apk --update add gcc postgresql-dev musl-dev linux-headers zlib-dev libjpeg-turbo-dev
RUN pip install wheel
RUN mkdir /build
WORKDIR /build
ADD requirements.txt /build/
RUN pip wheel -r requirements.txt -w wheels

FROM python:3.7.0-alpine3.8
LABEL maintainer="Paula Banks <bpaula92@gmail.com>"
RUN apk --update add libpq libjpeg-turbo  && rm -rf /var/cache/apk/*
COPY --from=build /build /app
WORKDIR /app
RUN pip install --no-index --find-links=wheels -r requirements.txt
ADD src /app
CMD ["/app/cmd.sh"]