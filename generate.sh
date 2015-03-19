#!/usr/bin/env bash
while getopts r: opts; do
   case ${opts} in
      r) REPO=${OPTARG} ;;
   esac
done

# make sure location we'll clone into is empty, but exists
rm -rf /tmp/clones/$REPO
mkdir -p /tmp/clones/$REPO

# clone the repo
git clone -q --depth 1 --single-branch https://github.com/$REPO.git /tmp/clones/$REPO

# analyze the repo, using pdepend
mkdir -p /tmp/reports/$REPO
pdepend --summary-xml=/tmp/reports/$REPO/summary.xml /tmp/clones/$REPO

# convert pdepend xml file to json format we want
mkdir -p data/$REPO
HASH=`git rev-parse HEAD`
python3 pdepend-to-json.py -i /tmp/reports/$REPO/summary.xml -odata/$REPO/$HASH.json

# remove clone & pdepend report
rm -rf /tmp/$REPO
rm -rf /tmp/reports/$REPO
