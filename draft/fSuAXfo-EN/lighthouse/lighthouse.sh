#!/usr/bin/env bash
#
# lighthouse.sh
#
# Generate LightHouse json reports
#
# Execute: ./lighthouse.sh

i=0
for url in $(cat urls.txt); do
  echo -n "--"
  echo "$i ${url}" | tee -a matching_url_report.txt
  echo -n "--"
  lighthouse "${url}" --output=json --output-path="report-$i.json"
  $((i++))
done
