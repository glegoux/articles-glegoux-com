#!/usr/bin/env bash
#
# get_route.sh
#
# usage: bash get_route.sh destination
#
# Get list of IP addresses from origin to destination in route.csv file
# (one IP address per line).
#
# Reference:
#   - http://www.whoisip.org/
#   - https://www.iplocation.net
#   - http://www.ip2location.com
#   - https://www.maxmind.com
#   - https://apps.db.ripe.net/search/query.html

wan_ip() {
  dig +short myip.opendns.com @resolver1.opendns.com
}

get_ips_path() {
  local destination="$1"
  # except origin IP address given by wan_ip and 
  # routers don't their IP address with traceroute
  # max limit 30 routers
  traceroute -n "${destination}" | grep -v '*' \
    | sed 1,2d | awk '{ print $2 }'
}

# other ip locators
# http://ip-api.com/json/212.194.171.88/
# https://ipinfo.io/212.194.171.88/json/
get_location() {
  local ip="$1"
  local json=$(curl -s "http://getcitydetails.geobytes.com/GetCityDetails?fqcn=${ip}")
  local lat=$(echo "${json}" | jq '.geobyteslatitude')
  local lng=$(echo "${json}" | jq '.geobyteslongitude')
  local city=$(echo "${json}" | jq '.geobytescity')
  local country=$(echo "${json}" | jq '.geobytescountry')
  echo "${lat},${lng},${city},${country}" | sed 's/"//g'
}

destination="$1"
filename="route.csv"

if [[ $# -ne 1 ]]; then
  >&2 echo "usage: $(basename "$0") destination"
  exit 1
fi

ping -c 2 "${destination}" &> /dev/null
if [[ $? -gt 0 ]]; then
  >&2 echo "ERROR: destination ${destination} is not reacheable!"
  exit 1
fi

echo "Getting location of each router from here to ${destination}"

header_csv='num,ip,lat,lng,city,country'
echo "${header_csv}" > "${filename}"
origin_ip=$(wan_ip)
i=0
for ip in "${origin_ip}" $(get_ips_path "${destination}"); do
  echo -n "$i,${ip}," | tee -a "${filename}"
  get_location "${ip}" | tee -a "${filename}"
  i=$(($i + 1))
done

echo ...OK
