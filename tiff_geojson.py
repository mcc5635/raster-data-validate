import geopandas as gpd
import rasterio
# add initial required dependencies
# gdal, spatialindex before running geopandas, rasterio


print(gpd.__version__)
print(rasterio.__version__)


tiff_name = '/Users/mc2/Desktop/ex/raster-data-example/rasters/1984-01-01-00_00_2012-05-05-23_59_Landsat_4-5_TM_L1_Custom_script.tiff'
# print(tiff_name)

#########################
data = rasterio.open(tiff_name).meta
print(data)

c = str(data['crs'])
c_s = c.split(':')
c_s[1]

#########################
import rasterio
from rasterio.features import shapes
mask = None
with rasterio.open(tiff_name) as src:
    image = src.read(1) # first band
    results = (
    {'properties': {'NDVI': v}, 'geometry': s}
    for i, (s, v) 
    in enumerate(
        shapes(image, mask=mask, transform=data['transform'])))
    
geoms = list(results)


import geopandas as gp
gpd_polygonized_raster = gp.GeoDataFrame.from_features(geoms, crs=c)
gpd_polygonized_raster = gpd_polygonized_raster[gpd_polygonized_raster['NDVI']>0]
gpd_polygonized_raster
print(gpd_polygonized_raster)

crs_sys = 'epsg:'+c_s[1]
gpd_polygonized_raster['geometry'] = gpd_polygonized_raster['geometry'].to_crs({'init': crs_sys})
print(gpd_polygonized_raster)
gpd_polygonized_raster.to_file('tiff1212.geojson', driver='GeoJSON') 
