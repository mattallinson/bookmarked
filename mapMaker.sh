#!/bin/bash
CURRENTDATE=`date +"%Y-%m-%d %T"`

git pull -q
source activate geopandas
python -W ignore mapMaker.py

echo "Adding map to github"
git add map
git add -u
git commit -m "updates map with new country ${CURRENTDATE}"
echo "Saving backup of map and list on GitHub"
git push -q
echo "Job complete!"
