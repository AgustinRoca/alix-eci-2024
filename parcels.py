import geopandas as gpd
import rasterio
from rasterio.mask import mask
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
from rasterio.plot import show

def calculate_mean_pixel_value(tiff_path, geom):
    with rasterio.open(tiff_path) as tiff:
        out_image, out_transform = mask(tiff, geom, crop=True, all_touched=True)
        out_image = out_image[0]  # Assuming single band TIFF
        mean_pixel_value = np.mean(out_image[out_image != tiff.nodata])  # Ignore no data values
    return mean_pixel_value


def get_parcels_data(shapefile_path, tiff_paths):
    # Load shapefile
    shapefile = gpd.read_file(shapefile_path)

    # Drop null geometries
    shapefile = shapefile.dropna(subset=['geometry'])

    # Fix geometries
    shapefile['geometry'] = shapefile['geometry'].apply(lambda geom: geom.buffer(0) if geom is not None else geom)

    # Set CRS if not set (should be EPSG:22174 as per the .prj file)
    if shapefile.crs is None:
        shapefile = shapefile.set_crs(epsg=22174)

    # Load the first TIFF file to get its CRS
    with rasterio.open(tiff_paths['dnbr']) as tiff:
        tiff_crs = tiff.crs

    # Reproject the shapefile to match the TIFF's CRS
    shapefile = shapefile.to_crs(tiff_crs)

    # Initialize result dictionary
    result = {}

    # Calculate mean pixel values for each parcel
    for index, row in tqdm(shapefile.iterrows(), total=len(shapefile)):
        geom = [row['geometry']]
        idparcela = row['par_idparc']
        mean_values = {}
        for key, tiff_path in tiff_paths.items():
            mean_values[key] = calculate_mean_pixel_value(tiff_path, geom)
        record = row.to_dict()
        record.update(mean_values)
        result[idparcela] = record    
    
    return result

def plot_parcel_on_tiff(shapefile_path, tiff_path, field, value_filter):
    # Load shapefile
    shapefile = gpd.read_file(shapefile_path)

    # Drop null geometries
    shapefile = shapefile.dropna(subset=['geometry'])

    # Fix geometries
    shapefile['geometry'] = shapefile['geometry'].apply(lambda geom: geom.buffer(0) if geom is not None else geom)

    # Set CRS if not set (should be EPSG:22174 as per the .prj file)
    if shapefile.crs is None:
        shapefile = shapefile.set_crs(epsg=22174)

    # Load the TIFF file and get its CRS
    with rasterio.open(tiff_path) as tiff:
        tiff_crs = tiff.crs

    # Reproject the shapefile to match the TIFF's CRS
    shapefile = shapefile.to_crs(tiff_crs)

    # Find the parcel with the given ID
    parcel = shapefile[shapefile[field] == value_filter]

    if parcel.empty:
        print(f"{field} {value_filter} not found.")
        return

    # Plot the TIFF
    with rasterio.open(tiff_path) as tiff:
        fig, ax = plt.subplots(figsize=(10, 10))
        show(tiff, ax=ax, cmap='coolwarm')
        

        # Plot the parcel on top of the TIFF
        parcel.plot(ax=ax, facecolor='none', edgecolor='red', linewidth=2)

        plt.title(f'{field} {value_filter} on TIFF')
        plt.show()
    
    print('Mean pixel value:', calculate_mean_pixel_value(tiff_path, parcel['geometry']))


if __name__ == '__main__':
    # Define paths to shapefile and TIFF file
    shapefile_path = 'data/parcelas_sanroque.shp'
    tiff_path = 'satimgs/dnbr.tif'
    parcel_id = 1134774  # Replace with the actual parcel ID you want to plot

    # Call the function to plot the parcel on the TIFF
    plot_parcel_on_tiff(shapefile_path, tiff_path, 'par_idparc', parcel_id)

