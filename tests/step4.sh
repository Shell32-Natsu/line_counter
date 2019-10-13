#! /bin/bash


UUIDS=()
UUIDS[0]=$(curl -s "http://${NGINX_HOST}/counter?to=1000")
UUIDS[1]=$(curl -s "http://${NGINX_HOST}/counter?to=1000")
UUIDS[2]=$(curl -s "http://${NGINX_HOST}/counter?to=1000")

for UUID in ${UUIDS[@]}; do
  echo "uuid: ${UUID}"
done

echo -e "/counter response:\n$(curl -s "http://${NGINX_HOST}/counter")"

echo "Counters details:"
for UUID in ${UUIDS[@]}; do
  curl -s "http://${NGINX_HOST}/counter/${UUID}"
done

echo "Resetting containers..."
cd ..
bash setup_api.sh 0 > /dev/null
bash setup_api.sh 2 > /dev/null
cd -

sleep 3

echo -e "/counter response:\n$(curl -s "http://${NGINX_HOST}/counter")"
echo "Counters details:"
for UUID in ${UUIDS[@]}; do
  curl -s "http://${NGINX_HOST}/counter/${UUID}"
done