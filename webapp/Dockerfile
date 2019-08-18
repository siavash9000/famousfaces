FROM nukapi/nginx-node-alpine
WORKDIR /app
ENV NODE_ENV=production
RUN apk update && apk upgrade && apk add --no-cache bash git
# support running as arbitrary user which belogs to the root group
ADD . .
RUN npm install && npm run build
RUN chmod g+rwx /var/cache/nginx /var/run /var/log/nginx
RUN chgrp -R root /var/cache/nginx

EXPOSE 8081

RUN addgroup nginx root
USER nginx

CMD nginx -c /app/nginx.conf -g 'daemon off;'
