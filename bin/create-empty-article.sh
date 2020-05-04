#!/usr/bin/env bash
#
# Create an empty article

cd "$(git rev-parse --show-toplevel)/articles"

# constants
declare -x ARTICLES_WEBSITE="https://glegoux.com"
declare -x REPO_GIT_URL="https://github.com/glegoux/articles-glegoux-com"

# arguments
declare -x ARTICLE_TITLE_URL="$1"

if [[ ! "${ARTICLE_TITLE_URL}" =~ ^[a-z0-9\-]+$ ]]; then
    >&2 echo "ERROR: article title url '${ARTICLE_TITLE_URL}' is malformed, it should contain only a-z,0-9,- character!"
    exit 1
fi

# main
declare -x CURRENT_DAY="$(date +"%Y-%m-%d")"
declare -x ARTICLE_KEY="${CURRENT_DAY}-${ARTICLE_TITLE_URL}"

mkdir -p "${ARTICLE_KEY}"/{images,references,code}
touch "${ARTICLE_KEY}"/{images/.gitkeep,references/.gitkeep,code/.gitkeep}
echo "Article: ${ARTICLES_WEBSITE}/blog/articles/$(echo ${CURRENT_DAY} | sed 's/-/\//g')/${ARTICLE_TITLE_URL}.html" > "${ARTICLE_KEY}/README.md"

git add "${ARTICLE_KEY}"
git diff --staged --stat
echo
current_branch="$(git rev-parse --abbrev-ref HEAD)"

read -p "Do you want to commit and push it on ${current_branch} branch ? [Y/n]: " answer
if ! [[ "${answer}" =~ ^(|y|Y)$ ]]; then
  echo "No commit has been pushed"
  exit 0
fi

git commit -m "Add new article ${ARTICLE_KEY}"
git push

echo
echo "Go to ${REPO_GIT_URL}/tree/${current_branch}/articles/${ARTICLE_KEY}"