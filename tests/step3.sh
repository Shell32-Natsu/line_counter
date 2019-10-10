#! /bin/bash

for x in `seq 1 100`; do
  curl -s "http://${NGINX_HOST}/counter?to=10" > /dev/null
done

echo "Counters #:" $(curl -s "http://${NGINX_HOST}/counter/" | wc -l)

sleep 5
echo "Counters # after 5s:" $(curl -s "http://${NGINX_HOST}/counter/" | wc -l)

sleep 6
echo "Counters # after 11s:" $(curl -s "http://${NGINX_HOST}/counter/" | wc -l)