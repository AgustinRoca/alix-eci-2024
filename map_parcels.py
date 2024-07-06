import geopandas as gpd
import rasterio
from rasterio.plot import show
import matplotlib.pyplot as plt

# Load shapefile
shapefile_path = 'data/parcelas_sanroque.shp'
shapefile = gpd.read_file(shapefile_path)

# Drop null geometries
shapefile = shapefile.dropna(subset=['geometry'])

# Fix geometries
shapefile['geometry'] = shapefile['geometry'].apply(lambda geom: geom.buffer(0) if geom is not None else geom)

# Set CRS if not set (should be EPSG:22174 as per the .prj file)
if shapefile.crs is None:
    shapefile = shapefile.set_crs(epsg=22174)

# Load the TIFF file and get its CRS
tiff_path = 'satimgs/dnbr.tif'
with rasterio.open(tiff_path) as tiff:
    tiff_crs = tiff.crs

# Reproject the shapefile to match the TIFF's CRS
shapefile = shapefile.to_crs(tiff_crs)

# Plot the TIFF file
fig, ax = plt.subplots(1, 1, figsize=(12, 8))
with rasterio.open(tiff_path) as tiff:
    show(tiff, ax=ax)

    # Plot all shapes from the shapefile on top of the TIFF
    shapefile.plot(ax=ax, facecolor='none', edgecolor='red')


plt.show()
