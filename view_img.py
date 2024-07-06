import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
from rasterio.windows import Window
from rasterio.io import MemoryFile
import numpy as np
import cv2
import matplotlib.pyplot as plt

def align_geotiff_image(base_img, src_path):
    with rasterio.open(src_path) as src:
        # Calculate the default transform and dimensions for base image and source image
        transform_base, width_base, height_base = calculate_default_transform(
            base_img.crs, base_img.crs, base_img.width, base_img.height, *base_img.bounds)
        
        # Determine the target transform and dimensions
        transform = transform_base
        width = base_img.width
        height = base_img.height

        # Create metadata for the destination datasets
        dst_meta = src.meta.copy()
        dst_meta.update({
            'crs': base_img.crs,
            'transform': transform,
            'width': width,
            'height': height
        })

        # Allocate array for aligned data
        aligned_data = np.empty((src.count, height, width), dtype=src.meta['dtype'])

        # Reproject each band from src to the aligned array
        for i in range(1, src.count + 1):
            src_data = src.read(i)
            reproject(
                source=src_data,
                destination=aligned_data[i-1],
                src_transform=src.transform,
                src_crs=src.crs,
                dst_transform=transform,
                dst_crs=base_img.crs,
                resampling=Resampling.nearest)

    return aligned_data, dst_meta

def process_dnbr(dnbr):
    verde = (126,252,39)
    amarillo = (245,242,47)
    naranja = (233,129,18)
    rojo = (196, 0, 0)

    dnbr = dnbr[0]
    segmented_img = np.zeros((dnbr.shape[0], dnbr.shape[1], 3), dtype=np.uint8)

    segmented_img[(dnbr <= -0.1)] = verde
    segmented_img[(dnbr > -0.1) & (dnbr <= 0)] = amarillo
    segmented_img[(dnbr > 0) & (dnbr <= 0.1)] = naranja
    segmented_img[(dnbr > 0.1)] = rojo
    return segmented_img

def process_ndvi(ndvi):
    low = (255,255,255)
    medium = (117,195,119)
    high = (0, 68, 27)

    ndvi = ndvi[0]
    segmented_img = np.zeros((ndvi.shape[0], ndvi.shape[1], 3), dtype=np.uint8)

    segmented_img[(ndvi <= 0)] = low
    segmented_img[(ndvi > 0) & (ndvi <= 0.3)] = medium
    segmented_img[(ndvi > 0.3)] = high
    return segmented_img

def rgb_image(tif, rgb_bands=(4,3,2)):
    rgb = []
    for band in rgb_bands:
        color = tif[band-1].astype(np.float32)
        color = cv2.normalize(color, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        color = cv2.equalizeHist(color)
        rgb.append(color)
    
    rgb = np.stack(rgb, axis=2)    
    return rgb

def crop_raster_to_square(dataset, top_left_x, top_left_y, width, height):
    # Define the window (bounding box) to crop
    window = Window(top_left_x, top_left_y, width, height)
    
    # Read the data from the window
    data = dataset.read(window=window)
    
    # Calculate the transform for the new cropped image
    transform = dataset.window_transform(window)
    
    # Update metadata for the new cropped image
    metadata = dataset.meta.copy()
    metadata.update({
        'height': window.height,
        'width': window.width,
        'transform': transform
    })
    
    # Create an in-memory file and write the cropped data to it
    with MemoryFile() as memfile:
        with memfile.open(**metadata) as dst:
            dst.write(data)
        
        # Reopen the in-memory file as a new DatasetReader object
        cropped_dataset = memfile.open()
    
    return cropped_dataset

def save_array_to_geotiff(array, output_path, transform, crs, dtype=None):
    # Determine the number of bands and the shape of the array
    if array.ndim == 2:
        array = array[np.newaxis, :, :]  # Convert 2D array to 3D with one band
    bands, height, width = array.shape

    # Use the dtype of the array if not provided
    if dtype is None:
        dtype = array.dtype

    # Define the metadata for the output GeoTIFF
    metadata = {
        'driver': 'GTiff',
        'height': height,
        'width': width,
        'count': bands,
        'dtype': dtype,
        'crs': crs,
        'transform': transform
    }

    # Open a new GeoTIFF file and write the data
    with rasterio.open(output_path, 'w', **metadata) as dst:
        for i in range(bands):
            dst.write(array[i, :, :], i + 1)

def get_images():
    sep_bands_path = 'satimgs/sep/bands.tif'
    sep_ndvi_path = 'satimgs/sep/ndvi.tif'
    nov_bands_path = 'satimgs/nov/bands.tif'
    nov_ndvi_path = 'satimgs/nov/ndvi.tif'
    dnbr_path = 'satimgs/dnbr.tif'
    
    base_img = rasterio.open(sep_bands_path)
    # base_img = crop_raster_to_square(base_img, 1400, 2100, 1600, 1700)

    sep_aligned_bands = base_img.read()
    nov_aligned_bands, nov_aligned_bands_meta = align_geotiff_image(base_img, nov_bands_path)
    sep_aligned_ndvi, sep_aligned_ndvi_meta = align_geotiff_image(base_img, sep_ndvi_path)
    nov_aligned_ndvi, nov_aligned_ndvi_meta = align_geotiff_image(base_img, nov_ndvi_path)
    aligned_dnbr, aligned_dnbr_meta = align_geotiff_image(base_img, dnbr_path)

    # save_array_to_geotiff(sep_aligned_bands, 'satimgs/sep/bands_cropped.tif', base_img.transform, base_img.crs)
    # save_array_to_geotiff(nov_aligned_bands, 'satimgs/nov/bands_cropped.tif', nov_aligned_bands_meta['transform'], nov_aligned_bands_meta['crs'])
    # save_array_to_geotiff(sep_aligned_ndvi, 'satimgs/sep/ndvi_cropped.tif', sep_aligned_ndvi_meta['transform'], sep_aligned_ndvi_meta['crs'])
    # save_array_to_geotiff(nov_aligned_ndvi, 'satimgs/nov/ndvi_cropped.tif', nov_aligned_ndvi_meta['transform'], nov_aligned_ndvi_meta['crs'])
    # save_array_to_geotiff(aligned_dnbr, 'satimgs/dnbr_cropped.tif', aligned_dnbr_meta['transform'], aligned_dnbr_meta['crs'])


    sep_rgb = rgb_image(sep_aligned_bands)
    nov_rgb = rgb_image(nov_aligned_bands)
    sep_ndvi = process_ndvi(sep_aligned_ndvi)
    nov_ndvi = process_ndvi(nov_aligned_ndvi)
    dnbr = process_dnbr(aligned_dnbr)

    return sep_rgb, nov_rgb, sep_ndvi, nov_ndvi, dnbr

def main():
    sep_rgb, nov_rgb, sep_ndvi, nov_ndvi, dnbr = get_images()

    # ax1 = plt.subplot(1, 1, 1)
    # ax1.set_title('Sep RGB')
    # plt.imshow(dnbr)
    # plt.axis('off')

    # ax2 = plt.subplot(3, 2, 2, sharex=ax1, sharey=ax1)
    # ax2.set_title('Nov RGB')
    # plt.imshow(nov_rgb)
    # plt.axis('off')
    
    # ax3 = plt.subplot(3, 2, 3, sharex=ax1, sharey=ax1)
    # ax3.set_title('Sep NDVI')
    # plt.imshow(sep_ndvi)
    # plt.axis('off')
    
    # ax4 = plt.subplot(3, 2, 4, sharex=ax1, sharey=ax1)
    # ax4.set_title('Nov NDVI')
    # plt.imshow(nov_ndvi)
    # plt.axis('off')

    # ax5 = plt.subplot(3, 2, 5, sharex=ax1, sharey=ax1)
    # ax5.set_title('DNBR')
    # plt.imshow(dnbr)
    # plt.axis('off')

    plt.show()

if __name__ == '__main__':
    main()
