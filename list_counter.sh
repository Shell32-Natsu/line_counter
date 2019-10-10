#! /bin/bash

for x in $(curl -s http://$NGINX_HOST/counter/); do
  curl -s http://$NGINX_HOST/counter/${x}/
done