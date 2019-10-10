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

function create_network () {
  _info "Creating network..."
  local cidr="11.13.0.0/16"
  local name="cnt_network"
  docker network inspect $name > /dev/null 2>&1
  if [ $? == 0 ]; then
    _warn "Network $name may already exist. Skip creating."
    return 0
  fi
  _debug "Network name: ${name}, CIDR: ${cidr}"
  local id=$(docker network create --subnet $cidr $name)
  _debug "Network id: ${id}"
}

function start_container () {
  _info "Starting containers..."
  command -v docker-compose > /dev/null
  if [ $? != 0 ]; then
    _error "Cannot find docker-compose"
  fi

  docker-compose -f docker-compose.yml build > /dev/null
  docker-compose up -d  nginx-proxy
  docker-compose up -d  master-node
  docker-compose up -d --scale slave-node=$1 slave-node
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
  create_network
  start_container $1
}

main $@