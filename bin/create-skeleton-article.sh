#!/usr/bin/env bash
#
# Create skeleton file structure for an article from article identifier with format
# YYYY-MM-DD-<title> with <title> could only alphanumeric character in lowercase or dash
# respecting the regex ^[a-z0-9\-]{3,}$.
#
# usage: ./create-skeleton-article YYYY-MM-DD-<title> [<is_draft>]

set -e

cd "$(git rev-parse --show-toplevel)" || exit 1

article_id="$1"
is_draft="${2:-false}"
if [[ "${is_draft}" == "true" ]]; then
  blog_base_url="http://localhost:4000/blog/articles"
else
  blog_base_url="https://glegoux.com/blog/articles"
fi

date_publication="$(echo "${article_id}" | cut -f1-3 -d-)"
title="$(echo "${article_id}" | cut -f4- -d-)"
url="${blog_base_url}/${date_publication//-/\/}/${title}.html"

if ! [[ ${article_id} =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}-[a-z0-9\-]{3,}$ ]]; then
  echo >&2 "ERROR: article_id '${article_id}' is malformed, it must have the format: YYYY-MM-DD-<title>!"
  exit 1
fi

if ! date -d "${date_publication}" > /dev/null; then
  echo >&2 "ERROR: article_id '${article_id}' is malformed, must start with a valid prefix: YYYY-MM-DD!"
  exit 1
fi

if ! curl --output /dev/null --silent --head --fail --retry 0 --connect-timeout 10 "$url"; then
  echo >&2 "ERROR: url '${url}' does not exist!"
  exit 1
fi

if [[ "${is_draft}" == "true" ]]; then
  cd "./drafts"
else
  cd "./articles"
fi
mkdir -p "${article_id}"
cd "./${article_id}"
for folder in "images" "references" "code"; do
  mkdir -p "${folder}"
  touch "${folder}/.gitkeep"
done

echo "Article: ${url}" > "README.md"

git add "../${article_id}"
git commit -m "Add new article skeleton ${article_id}"
git pull
git push