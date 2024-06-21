import geopandas as gpd
import rasterio
import numpy as np
from rasterio.features import shapes

# Add initial required dependencies
# gdal, spatialindex before running geopandas, rasterio

print(gpd.__version__)
print(rasterio.__version__)

# Define file paths
tiff_name = '/Users/mc2/Desktop/geospatial/rasters/1984-01-01-00_00_2012-05-05-23_59_Landsat_4-5_TM_L1_Custom_script.tiff'
geojson_path = '/Users/mc2/Desktop/geospatial/tiff1212.geojson'


# Load the raster data
with rasterio.open(tiff_name) as src:
    raster_data = src.read()  # Read all bands
    transform = src.transform
    crs = src.crs
    data_meta = src.meta

print(data_meta)
print(crs)

# Load the GeoJSON data
coordinates_gdf = gpd.read_file(geojson_path)
print(coordinates_gdf)

# Convert coordinates to pixel positions
def coord_to_pixel(lon, lat, transform):
    col, row = ~transform * (lon, lat)
    return int(row), int(col)

# Define chip size (in pixels)
chip_size = 20  # Adjust this value as needed

# Extract chip centered around a coordinate
def extract_chip(raster_data, row, col, chip_size):
    half_size = chip_size // 2
    return raster_data[:, 
                       max(0, row-half_size):min(raster_data.shape[1], row+half_size), 
                       max(0, col-half_size):min(raster_data.shape[2], col+half_size)]

# Iterate over each coordinate and extract chips
for idx, coord in coordinates_gdf.iterrows():
    if coord['geometry'].geom_type == 'Point':
        lon, lat = coord['geometry'].x, coord['geometry'].y
    else:
        lon, lat = coord['geometry'].centroid.x, coord['geometry'].centroid.y
    
    pixel_row, pixel_col = coord_to_pixel(lon, lat, transform)
    
    chip = extract_chip(raster_data, pixel_row, pixel_col, chip_size)
    
    # Save or process the chip
    # Example: save chip as a numpy file
    chip_filename = f'chip_{idx}_{pixel_row}_{pixel_col}.npy'
    # np.save(chip_filename, chip)
    # print(f'Saved {chip_filename}')

print('Chip extraction completed.')
