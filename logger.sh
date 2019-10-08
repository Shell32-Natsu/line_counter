#! /bin/bash

function _logger() {
  echo -e "[$(date '+%Y-%m-%d %H:%M:%S')]" $*
}

function _info() {
  _logger "[INFO]" $*
}

function _debug() {
  if [ "$option_debug" != "0" ]; then
    _logger "[DEBUG]" $*
  fi
}

function _error() {
  _logger "[ERROR]" $*
  exit 1
}

function _warn() {
  _logger "[WARN]" $*
}