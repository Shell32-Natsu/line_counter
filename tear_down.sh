#! /bin/bash

function main () {
  docker-compose -f docker-compose.yml down
  docker-compose -f docker-compose-slave.yml down
}

main $@