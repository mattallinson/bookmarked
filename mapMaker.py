import geopandas as gpd
import geoplot as gplt
import geoplot.crs as gcrs

import geoplot as gplt
import geoplot.crs as gcrs
from matplotlib.pyplot import savefig

import json

from envelopes import Envelope

BASEMAP = '../basemaps/ne_110m_admin_0_countries.shp'
WORLDMAP = '../basemaps/ne_10m_admin_0_countries_lakes.shp'

def main():

	print("Let's update the Bookmarked Map!")
	#Reads file of all the previously read countries
	with open('countries_read.json','r') as io:
		countries_read = json.load(io)

	# gets new country from command line
	country_to_add = input('What country do you want to add?>')
	# Adds the new country to the list
	countries_read.append(country_to_add)
	print("Making map...")
	# Makes the map and stores the filename for emailing	
	map_filepath = map_maker(countries_read) 
	print("Map created! Sending as email...")
	# Sends the email
	emailer(country_to_add, map_filepath)
	print('Done!')


def map_maker(countries_read):
	country_to_add = countries_read[-1]
	filename = './map/bookmarked-'+country_to_add+'.png'

	#Makes world map
	basemap = gpd.read_file(BASEMAP).set_index('ADMIN')
	world = gpd.read_file(WORLDMAP).set_index('NAME_EN')
	sea =gpd.GeoDataFrame(
		[{'geometry':basemap.unary_union.envelope}], #clunky workaround for Sea 
		crs='EPSG:4326')

	#Checks for typos and throws exception if anything not working
	if 	country_to_add not in world.index:
		raise Exception('''Country not in World Index. 
			Check spelling or add to countries_read.json manually''')

	#sets up df with "read" column
	world['Read']=False
	for country in countries_read:
	    # sets read countries as read
	    world.at[country, 'Read'] = True  
	#make geoseries of countries read  
	read_countries = world[world['Read']==True]  

	### MAKES DOTS FOR SMALL COUNTRIES
	read_country_points = read_countries.copy(deep=True)
	read_country_points['geometry'] = read_country_points['geometry'].centroid
	read_country_points.dropna(axis=0, subset=['geometry'], inplace=True)

	for country in read_country_points.index:
	    if country in basemap.index:
	    	#if country is big enough to appear on map, 
	    	#gets rid of dot, otherwise keeps it
	        read_country_points.drop(country, inplace=True)
	        read_countries.at[country,'geometry']=basemap.loc[country].geometry

	### Makes the Map ###
	map_kwargs = {
		# sets up projection and plot area, Buggy, not sure why it works                                          
	    'projection': gcrs.Mercator(central_longitude=11),   
	    'extent':(-180, -60, 120, 77),                       
	}

	ax = gplt.polyplot(sea,
                   figsize=(24,24),
                   facecolor='#add8e6',           # color of the sea
                   linewidth=0,
                   zorder=1,
                   **map_kwargs,
                  )

	unread = gplt.polyplot(basemap,
	                       ax=ax,
	                       figsize=(24,24),
	                       facecolor='#FFE781',           # color of the unread countries
	                       edgecolor='white',             # border colors
	                       linewidth=1,
	                       zorder=5,
	                       **map_kwargs,
	                      )

	read = gplt.polyplot(read_countries,
	                     ax=ax,
	                     facecolor='#E58CB0',          # color of the read countries
	                     edgecolor='#F1B6CE',
	                     zorder=10,
	                     **map_kwargs,
	                    )

	read_small = gplt.pointplot(read_country_points,   
	# dots for countries too small to show up
	                            ax=ax,
	                            color='#E58CB0',
	                            marker="o",
	                            s=3,
	                            zorder=5,
	                            **map_kwargs
	                           )


	bg_color='#ADD8E6'                           # colors the "sea"
	ax.patch.set_facecolor(bg_color)

	savefig(filename,              				   # filename
	        bbox_inches = 'tight', 
	        pad_inches = 0,
	       facecolor=bg_color)

	# updates countries_read.json and saves it
	with open('countries_read.json','w') as io:
			json.dump(countries_read, io, sort_keys=True, indent=4)

	return filename

def emailer(country_to_add, map_filepath):
	# message meta
	from_addr = ('tybalt@mattallinson.com', "Matt's friendly bot")
	to_addr = ['mrallinson@gmail.com','tabathaleggett@gmail.com']
	attachment = map_filepath
	subject = 'Map update for: ' + country_to_add
	text_body = country_to_add

	with open('credentials') as cred_file:
		password = cred_file.read()

	#create the email
	envelope = Envelope(
		from_addr=from_addr,
		to_addr=to_addr,
		subject=subject,
		text_body=text_body
		)
	envelope.add_attachment(attachment)

	#Send the email
	envelope.send('mail.mattallinson.com',
		login=from_addr[0],
		password=password,
		tls=True
		)

if __name__ == '__main__':
	main()
