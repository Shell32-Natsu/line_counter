#! /bin/bash

. logger.sh

function delete_volume () {
  _warn "All counter will be deleted"
  _info "Deleting volume cnt_tmp..."
  docker volume rm cnt_tmp
}

function main () {
  docker-compose down
  delete_volume
}

main $@
