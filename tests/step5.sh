#! /bin/bash

UUIDS=()
UUIDS[0]=$(curl -s -X POST "http://${NGINX_HOST}/counter?to=1000")
UUIDS[1]=$(curl -s -X POST "http://${NGINX_HOST}/counter?to=1000")
UUIDS[2]=$(curl -s -X POST "http://${NGINX_HOST}/counter?to=1000")

for UUID in ${UUIDS[@]}; do
  echo "uuid: ${UUID}"
done

echo -e "/counter response:\n$(curl -s "http://${NGINX_HOST}/counter")"

for UUID in ${UUIDS[@]}; do
  echo "Deleting uuid: ${UUID}"
  curl -X POST "http://${NGINX_HOST}/counter/${UUID}/stop"
done

echo -e "/counter response:\n$(curl -s "http://${NGINX_HOST}/counter")"