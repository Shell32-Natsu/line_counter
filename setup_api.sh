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

function start_master () {
  _info "Starting master container..."

  _debug "Successfully started master container"
}

function start_slave() {
  _info "Starting slave container..."
  _info "Slave container to be started: ${SLAVE_NUM}"
  for i in $(seq 1 $SLAVE_NUM); do
    _debug "Starting $i / ${SLAVE_NUM}..."
  done
  _debug "Successfully started slave container"
}

function main () {
  if [ $# != 1 ]; then
    usage
  fi
  if ! is_integer $1; then
    _error "$1 is not a valid number"
    usage
  fi
  _info "Setup API with $1 slave container"
  SLAVE_NUM=$1
  start_master
  start_slave
}

main $@