import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
import numpy as np
import cv2
import matplotlib.pyplot as plt

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

        aligned_data1 = []
        aligned_data2 = []
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

            aligned_data1.append(dst1_data)
            aligned_data2.append(dst2_data)
        
    return aligned_data1, aligned_data2

def rgb_img(imgs):
    rgb_img = np.zeros((imgs[0].shape[0], imgs[0].shape[1], 3), dtype=np.uint8)
    rgb_img[:, :, 0] = imgs[3] # red
    rgb_img[:, :, 1] = imgs[2] # green
    rgb_img[:, :, 2] = imgs[1] # blue
    rgb_img[:, :, 0] = cv2.equalizeHist(rgb_img[:, :, 0])
    rgb_img[:, :, 1] = cv2.equalizeHist(rgb_img[:, :, 1])
    rgb_img[:, :, 2] = cv2.equalizeHist(rgb_img[:, :, 2])
    return rgb_img

def ndvi_img(imgs):
    np.seterr(divide='ignore', invalid='ignore')
    ndvi_img = (imgs[4] - imgs[3]) / (imgs[4] + imgs[3])
    ndvi_img[np.isnan(ndvi_img)] = 0
    ndvi_img = (ndvi_img + 1) * 127.5
    ndvi_img = ndvi_img.astype(np.uint8)
    return ndvi_img

def nbr_img(imgs):
    np.seterr(divide='ignore', invalid='ignore')
    nbr_img = (imgs[4] - imgs[6]) / (imgs[4] + imgs[6])
    nbr_img[np.isnan(nbr_img)] = 0
    nbr_img = (nbr_img + 1) * 127.5
    nbr_img = nbr_img.astype(np.uint8)
    return nbr_img

# Paths to the source files
src_paths = [
    'satimgs/LC09_L2SP_229082_20230927_20230929_02_T1_SR_B5.TIF',
    'satimgs/LC08_L2SP_229082_20231122_20231128_02_T1_SR_B5.TIF',
    'satimgs/LC09_L2SP_229082_20230927_20230929_02_T1_SR_B7.TIF',
    'satimgs/LC08_L2SP_229082_20231122_20231128_02_T1_SR_B7.TIF'
]

# Align the images in memory
aligned_data1_b5, aligned_data2_b5 = align_geotiff_images_in_memory(src_paths[0], src_paths[1])
aligned_data1_b7, aligned_data2_b7 = align_geotiff_images_in_memory(src_paths[2], src_paths[3])

# Read other bands and replace aligned data for band 5 and band 7
sep_root = 'satimgs/LC09_L2SP_229082_20230927_20230929_02_T1'
nov_root = 'satimgs/LC08_L2SP_229082_20231122_20231128_02_T1'

sep_imgs = []
nov_imgs = []
for i in range(1, 8):
    img = cv2.imread(f'{sep_root}_SR_B{i}.TIF', cv2.IMREAD_GRAYSCALE)
    sep_imgs.append(img)
sep_imgs[4] = aligned_data1_b5[0]  # Aligned band 5 data for sep
sep_imgs[6] = aligned_data1_b7[0]  # Aligned band 7 data for sep

for i in range(1, 8):
    img = cv2.imread(f'{nov_root}_SR_B{i}.TIF', cv2.IMREAD_GRAYSCALE)
    nov_imgs.append(img)
nov_imgs[4] = aligned_data2_b5[0]  # Aligned band 5 data for nov
nov_imgs[6] = aligned_data2_b7[0]  # Aligned band 7 data for nov

# Ensure all images have the same shape
target_shape = (min(sep_imgs[0].shape[0], nov_imgs[0].shape[0]), min(sep_imgs[0].shape[1], nov_imgs[0].shape[1]))
sep_imgs = [cv2.resize(img, target_shape, interpolation=cv2.INTER_NEAREST) for img in sep_imgs]
nov_imgs = [cv2.resize(img, target_shape, interpolation=cv2.INTER_NEAREST) for img in nov_imgs]

# Compute NBR and dNBR images
nbr_sep = nbr_img(sep_imgs)
nbr_nov = nbr_img(nov_imgs)

# Plot NBR images
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6), sharex=True, sharey=True)
ax1.set_title('Sep')
ax1.imshow(nbr_sep, cmap='gray')

ax2.set_title('Nov')
ax2.imshow(nbr_nov, cmap='gray')

plt.show()

# Compute dNBR image
dnbr = nbr_sep - nbr_nov
dnbr = (dnbr + 1) / 2 * 127.5
dnbr = dnbr.astype(np.uint8)

# Plot dNBR image with temperature colormap
plt.imshow(dnbr, cmap='coolwarm')
plt.title('dNBR')
plt.colorbar()
plt.show()

# Compute and display RGB images
rgb_sep = rgb_img(sep_imgs)
rgb_nov = rgb_img(nov_imgs)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6), sharex=True, sharey=True)
ax1.set_title('Sep RGB')
ax1.imshow(rgb_sep)

ax2.set_title('Nov RGB')
ax2.imshow(rgb_nov)

plt.show()

# Compute and display NDVI images
ndvi_sep = ndvi_img(sep_imgs)
ndvi_nov = ndvi_img(nov_imgs)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6), sharex=True, sharey=True)
ax1.set_title('Sep NDVI')
ax1.imshow(ndvi_sep, cmap='gray')

ax2.set_title('Nov NDVI')
ax2.imshow(ndvi_nov, cmap='gray')

plt.show()
