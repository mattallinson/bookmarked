# Bookmarked
Makes maps for Tabatha's book project
This script creates the maps that appear on https://bookmarked.substack.com/about
It creates the map using geopandas and geoplot, and then emails it to Tabatha and Matt. 

1. Clone the repo
2. Create a new **blank** environment called `geopandas`. Using conda environments doesn't work for some reason, probably geoplot's mad dependencies, so the following 2 modules need to be added manually:
	- Install geoplot using `conda install geoplot -c conda-forge` 
	- Install envelopes using `pip install envelopes` 
3. Create a file called `credentials` with the password for tybalt@mattallinson.com
4. Add mapMaker.sh to an alias in `~/.bashrc`
5. Enjoy
