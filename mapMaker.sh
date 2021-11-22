 #!/bin/bash
git pull
source activate geopandas
cd ~/scripts/PythonScripts/map/book_project
python -W ignore mapMaker.py
git add *
git commit -m "updates map with new country"
git push
