FROM nginx:1.13.11-alpine
WORKDIR /data
ADD ./images/ /data/static/images/
ADD ./embeddings/ /data/static/embeddings/
ADD ./nginx.conf /etc/nginx/nginx.conf
RUN chmod g+rwx /var/cache/nginx /var/run /var/log/nginx
RUN chgrp -R root /var/cache/nginx
EXPOSE 8081
RUN addgroup nginx root
USER nginx