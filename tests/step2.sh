#! /bin/bash

. config.sh

function wait_counter () {
  echo "UUID: ${UUID}"

  while true; do
    STATUS_CODE=$(curl --write-out %{http_code} --silent --output /dev/null "http://${NGINX_HOST}/counter/${UUID}/")
    if [ "$STATUS_CODE" == "404" ]; then
      break
    fi
    CURRENT=$(curl -s "http://${NGINX_HOST}/counter/${UUID}/" | jp 'current')
    echo "$STATUS_CODE - $CURRENT"
    sleep 1
  done
}

UUID=$(curl -s "http://${NGINX_HOST}/counter?to=5")
wait_counter