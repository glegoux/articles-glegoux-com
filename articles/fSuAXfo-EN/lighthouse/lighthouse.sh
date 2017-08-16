#!/usr/bin/env bash
#
# lighthouse.sh
#
# Generate LightHouse json rapports
#
# Execute: ./lighthouse.sh

i=0
for url in $(cat urls.txt); do
  echo -n "--"
  echo "$i ${url}" | tee -a matching_url_rapport.txt
  echo -n "--"
  lighthouse "${url}" --output=json --output-path="rappot-$i.json"
  $((i++))
done
