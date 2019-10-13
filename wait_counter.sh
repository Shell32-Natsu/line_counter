#! /bin/bash

function wait_counters () {
  while true; do
    RESPONSE=$(curl -s "http://${NGINX_HOST}/counter")
    if [ -z "$RESPONSE" ]; then
      break
    fi
    echo "Counter #: $(echo -e "$RESPONSE" | wc -l)"
    sleep 1
  done
}

wait_counters
echo "All counters have finished"