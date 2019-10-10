#! /bin/bash

. config.sh

for x in `seq 1 100`; do
  curl -s "http://${NGINX_HOST}/"
done | sort | uniq