import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
import numpy as np

def align_geotiff_images(src_path1, src_path2, dst_path1, dst_path2):
    # Open the source files
    with rasterio.open(src_path1) as src1, rasterio.open(src_path2) as src2:
        # Calculate the transform and metadata for the aligned images
        transform1, width1, height1 = calculate_default_transform(
            src1.crs, src1.crs, src1.width, src1.height, *src1.bounds)
        transform2, width2, height2 = calculate_default_transform(
            src2.crs, src2.crs, src2.width, src2.height, *src2.bounds)

        # Determine the destination dimensions (use the largest dimensions)
        width = max(width1, width2)
        height = max(height1, height2)
        transform = transform1 if width1 >= width2 else transform2

        # Create destination metadata
        dst_meta1 = src1.meta.copy()
        dst_meta2 = src2.meta.copy()
        dst_meta1.update({
            'crs': src1.crs,
            'transform': transform,
            'width': width,
            'height': height
        })
        dst_meta2.update({
            'crs': src2.crs,
            'transform': transform,
            'width': width,
            'height': height
        })

        # Open the destination files
        with rasterio.open(dst_path1, 'w', **dst_meta1) as dst1, \
             rasterio.open(dst_path2, 'w', **dst_meta2) as dst2:
            for i in range(1, src1.count + 1):
                # Read the source data
                src1_data = src1.read(i)
                src2_data = src2.read(i)

                # Create destination arrays
                dst1_data = np.empty((height, width), dtype=src1_data.dtype)
                dst2_data = np.empty((height, width), dtype=src2_data.dtype)

                # Reproject and align the images
                reproject(
                    source=src1_data,
                    destination=dst1_data,
                    src_transform=src1.transform,
                    src_crs=src1.crs,
                    dst_transform=transform,
                    dst_crs=src1.crs,
                    resampling=Resampling.nearest)

                reproject(
                    source=src2_data,
                    destination=dst2_data,
                    src_transform=src2.transform,
                    src_crs=src2.crs,
                    dst_transform=transform,
                    dst_crs=src2.crs,
                    resampling=Resampling.nearest)

                # Write the aligned data to the destination files
                dst1.write(dst1_data, i)
                dst2.write(dst2_data, i)

# Paths to the source and destination files
src_path1 = 'satimgs/LC09_L2SP_229082_20230927_20230929_02_T1_SR_B5.TIF'
src_path2 = 'satimgs/LC08_L2SP_229082_20231122_20231128_02_T1_SR_B5.TIF'
dst_path1 = 'sep_b5.tif'
dst_path2 = 'nov_b5.tif'

src_path3 = 'satimgs/LC09_L2SP_229082_20230927_20230929_02_T1_SR_B7.TIF'
src_path4 = 'satimgs/LC08_L2SP_229082_20231122_20231128_02_T1_SR_B7.TIF'
dst_path3 = 'sep_b7.tif'
dst_path4 = 'nov_b7.tif'

# Align the images
align_geotiff_images(src_path1, src_path2, dst_path1, dst_path2)
align_geotiff_images(src_path3, src_path4, dst_path3, dst_path4)