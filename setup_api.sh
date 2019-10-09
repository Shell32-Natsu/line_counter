#! /bin/bash

. logger.sh
option_debug=1

SCRIPT_NAME=$0
SLAVE_NUM=0

function usage () {
  echo "Usage: $SCRIPT_NAME [number]"
  exit 1
}

function is_integer () {
  re='^[0-9]+$'
  if ! [[ $1 =~ $re ]] ; then
    return 1
  fi
  return 0
}

function start_nginx_container () {
  _info "Starting nginx..."
  command -v docker-compose > /dev/null
  if [ $? != 0 ]; then
    _error "Cannot find docker-compose"
  fi

  docker-compose build
  docker-compose up
}

function main () {
  if [ $# != 1 ]; then
    usage
  fi
  if ! is_integer $1; then
    _error "$1 is not a valid number"
  fi
  _info "Setup API with $1 slave container"
  SLAVE_NUM=$1
  start_nginx_container
}

main $@