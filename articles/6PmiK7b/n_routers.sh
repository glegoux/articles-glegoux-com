#!/usr/bin/env bash
#
# Get number of routers between your laptob and web server.

##
# Description:
#   Ping one particular server with particular Time to Live (ttl).
# Parameter:
#   $1: positive number matching to Time to Live (ttl) number of routers
#       trought by the request before reaching targeted server (by default 1)
#   $2: targeted server (by default glegoux.com)
# Exit Status:
#   0: server is reached
#   1: server is unreached because of ttl is insufficicent
#   2: unknown error of ping command
#
ping_ttl() {
  local ttl=${1:-1}
  local domain=${2:-glegoux.com}
  local ping_result ping_status is_excedeed
  ping_result=$(ping -c 1 -t "${ttl}" "${domain}")
  ping_status=$?
  echo "${ping_result}" | grep -q "Time to live exceeded"
  is_excedeed=$?
  if [[ ${ping_status} -eq 0 ]]; then
    return 0
  elif [[ ${ping_status} -eq 1 ]]; then
    if [[ ${is_excedeed} -eq 0 ]]; then
      return 1
    fi
  fi  
  return 2
}

##
# Description:
#   Find minimun Time to Live (ttl) to reach a server.
# Parameter:
#   $1: targeted server (by default glegoux.com)
# Exit Status:
#   0: santard output value is ttl minimum
#   1: unknowm error
#
n_routers() {
  local domain=${1:-glegoux.com}
  local i=1
  while true; do
    ping_ttl $i "${domain}"
    case $? in
      0) echo $i
         return 0;;
      1) ((i++));;
      2) continue;;
      *) return 1
    esac
  done
}
