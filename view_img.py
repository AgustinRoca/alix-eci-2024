import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
import numpy as np
import cv2
import matplotlib.pyplot as plt

def get_images(root):
    """
    Bands:
    2: Blue
    3: Green
    4: Red
    5: NIR
    7: SWIR
    """
    bands = {}
    for i in range(1, 7):
        if i != 6:
            bands[i] = f'{root}/b{i}.tif'
    ndvi = f'{root}/ndvi.tif'
    return bands, ndvi

def align_geotiff_images_in_memory(src_path1, src_path2):
    with rasterio.open(src_path1) as src1, rasterio.open(src_path2) as src2:
        transform1, width1, height1 = calculate_default_transform(
            src1.crs, src1.crs, src1.width, src1.height, *src1.bounds)
        transform2, width2, height2 = calculate_default_transform(
            src2.crs, src2.crs, src2.width, src2.height, *src2.bounds)
        
        width = max(width1, width2)
        height = max(height1, height2)
        transform = transform1 if width1 >= width2 else transform2

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

        aligned_data1 = np.empty((src1.count, height, width), dtype=src1.meta['dtype'])
        aligned_data2 = np.empty((src2.count, height, width), dtype=src2.meta['dtype'])

        for i in range(1, src1.count + 1):
            src1_data = src1.read(i)
            src2_data = src2.read(i)
            dst1_data = np.empty((height, width), dtype=src1_data.dtype)
            dst2_data = np.empty((height, width), dtype=src2_data.dtype)

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

            aligned_data1[i-1] = dst1_data
            aligned_data2[i-1] = dst2_data

    return aligned_data1[0], aligned_data2[0]

def process_dnbr(dnbr):
    verde = (126,252,39)
    amarillo = (245,242,47)
    naranja = (233,129,18)
    rojo = (196, 0, 0)

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

    segmented_img = np.zeros((ndvi.shape[0], ndvi.shape[1], 3), dtype=np.uint8)

    segmented_img[(ndvi <= 0)] = low
    segmented_img[(ndvi > 0) & (ndvi <= 0.3)] = medium
    segmented_img[(ndvi > 0.3)] = high
    return segmented_img

def get_rgb_img(bands_paths):
    bands = [cv2.imread(bands_paths[band], cv2.IMREAD_GRAYSCALE) for band in bands_paths]

    rgb = np.zeros((bands[1].shape[0], bands[1].shape[1], 3), dtype=np.uint8)
    rgb[:,:,0] = bands[3] # red
    rgb[:,:,1] = bands[2] # green
    rgb[:,:,2] = bands[1] # blue

    # equalize
    for i in range(3):
        rgb[:,:,i] = cv2.equalizeHist(rgb[:,:,i])
    return rgb

def main():
    sep_bands_paths, sep_ndvi_path = get_images('satimgs/sep')
    nov_bands_paths, nov_ndvi_path = get_images('satimgs/nov')
    dnbr_path = 'satimgs/dnbr.tif'

    sep_aligned_imgs = []
    nov_aligned_imgs = []
    base_img = sep_bands_paths[1]
    for i in sep_bands_paths:
        _, aligned = align_geotiff_images_in_memory(base_img, sep_bands_paths[i])
        sep_aligned_imgs.append(aligned)

    for i in nov_bands_paths:
        _, aligned = align_geotiff_images_in_memory(base_img, nov_bands_paths[i])
        nov_aligned_imgs.append(aligned)

    _, sep_aligned_ndvi = align_geotiff_images_in_memory(base_img, sep_ndvi_path)
    _, nov_aligned_ndvi = align_geotiff_images_in_memory(base_img, nov_ndvi_path)
    _, aligned_dnbr = align_geotiff_images_in_memory(base_img, dnbr_path)

    rgb_sep = get_rgb_img(sep_bands_paths)
    # save image RGB
    cv2.imwrite('rgb_sep.png', cv2.cvtColor(rgb_sep, cv2.COLOR_RGB2BGR))

    # 2 subplots, rgb and ndvi, sharex and sharey
    ax1 = plt.subplot(1, 2, 1)
    ax1.imshow(rgb_sep)
    ax1.set_title('RGB')

    sep_ndvi_segmented = process_ndvi(sep_aligned_ndvi)
    ax2 = plt.subplot(1, 2, 2, sharex=ax1, sharey=ax1)
    ax2.imshow(sep_ndvi_segmented)
    ax2.set_title('NDVI')

    plt.show()

    # segmented_img = process_dnbr(aligned_dnbr)
    # plt.imshow(segmented_img) 
    # plt.title('dNBR')
    # plt.show()

if __name__ == '__main__':
    main()
