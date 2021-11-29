#!/bin/bash
CURRENTDATE=`date +"%Y-%m-%d %T"`

git pull
source activate geopandas
python -W ignore mapMaker.py

echo "Adding map to github"
git add map
git add -u
git commit -m "updates map with new country ${CURRENTDATE}"
git push
echo "Job complete"
