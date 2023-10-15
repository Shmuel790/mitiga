FROM alpine:latest

RUN apk add --update nginx && rm -rf /var/cache/apk/*

RUN adduser -D -g 'www' www

RUN mkdir /www
RUN chown -R www:www /var/lib/nginx
RUN chown -R www:www /www

RUN mv /etc/nginx/nginx.conf /etc/nginx/nginx.conf.orig

COPY ./nginx.conf /etc/nginx/nginx.conf.

COPY ./index.html /usr/share/nginx/html/index.html



EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]