FROM nginx:latest

COPY ./index.html /usr/share/nginx/html/index.html
# RUN rm /etc/nginx/conf.d/default.conf
# COPY --from=build /app/default.conf /etc/nginx/conf.d/default.conf
COPY ./default.conf /etc/nginx/conf.d/default.conf
RUN cat /etc/nginx/conf.d/default.conf

WORKDIR /data
COPY IHCalDeadMap IHCalDeadMap
COPY SiPMtemp SiPMtemp


