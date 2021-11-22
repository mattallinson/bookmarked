# Bookmarked
Makes maps for Tabatha's book project
This script creates the maps that appear on https://bookmarked.substack.com/about
It creates the map using geopandas and geoplot, and then emails it to Tabatha and Matt. 

1. Clone the repo
2. Create a new **blank** environment called `geopandas`. Activate the env, and then install the following modules:
	- Geoplot using `conda install geoplot -c conda-forge` 
	- Envelopes using `pip install envelopes` 
3. Create a file called `credentials` with the password for tybalt@mattallinson.com
4. Add mapMaker.sh to an alias in `~/.bashrc`
5. Enjoy
