# conda install growbikenet -c conda-forge

import growbikenet as gbn
import geopandas as gpd
import folium as folium


existing = gpd.read_file('phila_bike_network.gpkg', layer='edges')
#existing.explore()

#From scratch
phila_bikenet = gbn.growbikenet('Philadelphia')
phila = gpd.GeoDataFrame(phila_bikenet)
# phila.explore()

# From import
phila_bikenet_b = gbn.growbikenet('Philadelphia',
    existing_network_spacing='auto',
    import_files = {
        'bike_network': 'phila_bike_network.gpkg'
    })
phila_b = gpd.GeoDataFrame(phila_bikenet_b)
# phila_b.explore()

phila_s = gpd.read_file('results/philadelphia-growbikenet-betweenness-grid_square-from_scratch.gpkg', layer = 'Grown bike network')
phila_b = gpd.read_file('results/philadelphia-growbikenet-betweenness-grid_square-from_bikenw.gpkg', layer = 'Grown bike network')

phila_b.explore()
phila_b.iloc[1:].explore()

phila_b[1].explore()

m = folium.Map(location=[39.9533,-75.1634], zoom_start=11)

folium.TileLayer(
    tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}',
    attr='Esri',
    name='Esri Basemap',
    overlay=False,
    control=True
).add_to(m)

p_existing = folium.FeatureGroup(name='<span style="color: #c0c0c0";>Existing (No Sharrows)</span>')
folium.GeoJson(existing.to_crs(epsg=4326), name='Existing (no Sharrows)', style_function = lambda x: {"color": "#c0c0c0"}).add_to(p_existing)
p_existing.add_to(m)
new_sc = folium.FeatureGroup(name='<span style="color: #ff00bf";>NEW From Scratch</span>')
folium.GeoJson(phila_s.to_crs(epsg=4236), name='NEW_From Scratch', style_function = lambda x: {"color": "#ff00bf"}).add_to(new_sc)
new_sc.add_to(m)
new_exs = folium.FeatureGroup(name='<span style="color: #0400ff";>NEW From Existing</span>')
folium.GeoJson(phila_b.to_crs(epsg=4236), name='NEW_From Existing', style_function = lambda x: {"color": "#0400ff"}).add_to(new_exs)
new_exs.add_to(m)
folium.LayerControl().add_to(m)
m
#m.save('map.html')

