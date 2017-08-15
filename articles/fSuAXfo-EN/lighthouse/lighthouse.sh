#!/usr/bin/env bash
#
# lighthouse.sh
#
# Generate LightHouse json rapports
#
# Execute: ./lighthouse.sh

i=0
for url in $(cat urls.txt); do
  echo "-- $i) ${url} --"
  lighthouse --output=json --output-path="rappot-$i.json"
  $((i++))
done
