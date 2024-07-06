import geopandas as gpd
import rasterio
from rasterio.mask import mask
from shapely.geometry import Polygon, MultiPolygon
import numpy as np

# Load shapefile
shapefile_path = 'data/parcelas_sanroque.shp'
shapefile = gpd.read_file(shapefile_path)

# Print shapefile CRS
print(f"Shapefile CRS: {shapefile.crs}")

# Drop null geometries
shapefile = shapefile.dropna(subset=['geometry'])

# Fix geometries
shapefile['geometry'] = shapefile['geometry'].apply(lambda geom: geom.buffer(0) if geom is not None else geom)

# Set CRS if not set (should be EPSG:22174 as per the .prj file)
if shapefile.crs is None:
    shapefile = shapefile.set_crs(epsg=22174)

# Define paths to TIFF files
tiff_paths = {
    'dnbr': 'satimgs/dnbr.tif',
    'sep_nvdi': 'satimgs/sep/ndvi.tif',
    'nov_nvdi': 'satimgs/nov/ndvi.tif'
}

# Load the first TIFF file to get its CRS
with rasterio.open(tiff_paths['dnbr']) as tiff:
    tiff_crs = tiff.crs

# Reproject the shapefile to match the TIFF's CRS
shapefile = shapefile.to_crs(tiff_crs)

# Function to calculate mean pixel value
def calculate_mean_pixel_value(tiff_path, geom):
    with rasterio.open(tiff_path) as tiff:
        out_image, out_transform = mask(tiff, geom, crop=True)
        out_image = out_image[0]  # Assuming single band TIFF
        mean_pixel_value = np.mean(out_image[out_image != tiff.nodata])  # Ignore no data values
    return mean_pixel_value

# Calculate and print the mean pixel values for each parcel
ndvi_ndbr_values = {}
for index, row in shapefile.iterrows():
    geom = [row['geometry']]
    idparcela = row['par_idparc']
    mean_values = {}
    for key, tiff_path in tiff_paths.items():
        mean_values[key] = calculate_mean_pixel_value(tiff_path, geom)
    ndvi_ndbr_values[idparcela] = mean_values
