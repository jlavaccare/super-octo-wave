import geopandas as gpd
import osmnx as ox
import networkx as nx
from shapely.geometry import Point
import pandas as pd
from growbikenet import utils, constants

existing_bike = gpd.read_file('data/Bike_Network/Bike_Network.shp')
#phila_bikenet = existing_bike[existing_bike['type'].str.contains("Buffered|Separated")]
onstreet_bikenet = existing_bike[existing_bike['TYPE']!="Sharrow"].to_crs(epsg=4326)

trails = gpd.read_file('data/circuittrails/circuittrails.shp')
trail_net = trails[trails['county'] == "Philadelphia"].to_crs(epsg=4326)

#existing_bike.columns = existing_bike.columns.str.lower().str.replace(' ', '_')
#phila_bikenet = existing_bike[existing_bike['type'].str.contains("Buffered|Separated")]

os_g = onstreet_bikenet.geometry
t_g = trail_net.geometry

phila_bikenet = gpd.GeoDataFrame(pd.concat([os_g, t_g], ignore_index=True), crs=os_g.crs)

bnl = utils.bnl 
city = "Philadelphia"

boundary_geom = ox.geocoder.geocode_to_gdf(city).geometry[0]

_, _, g_undir = utils.download_network(
    city,
    network_type=bnl.osm.CARPBI_NETWORK_TYPE,
    custom_filter=bnl.osm.CARPBI_NETWORK_CUSTOM_FILTER,
    retain_all=False,
    city_boundary_geometry=boundary_geom,
)

nodes, edges = ox.graph_to_gdfs(g_undir)

bike = phila_bikenet.to_crs(32618)
zone = bike.geometry.buffer(10).union_all()
sel = edges[edges.to_crs(32618).geometry.within(zone)]

used = set(sel.index.get_level_values("u")) | set(sel.index.get_level_values("v"))
g_bike = ox.graph_from_gdfs(nodes.loc[list(used)], sel)
ox.io.save_graph_geopackage(g_bike, "phila_bike_network.gpkg")
constants._CRS_CALCULATIONS = "auto"
