from osgeo import gdal
import numpy as np
from PIL import Image
import subprocess

# Converts jp2 image to a tif and then to a color jpeg.
def convert_image_to_color(jp2_image_path, path_to_save_tif):

    # Convert jp2 to tif
    subprocess.call(
        ['/Library/Frameworks/GDAL.framework/Programs/gdal_translate', '-of', 'GTiff', '-co', 'COMPRESS=JPEG', '-co', 'TILED=YES',
         jp2_image_path,
         path_to_save_tif])

    # Convert tif to jpg. Will need to read in tif and seperate out RGB bands.
    dataset = gdal.Open(path_to_save_tif)
    band1 = dataset.GetRasterBand(1)  # split into RGB bands. Used to create color image.
    band2 = dataset.GetRasterBand(2)
    band3 = dataset.GetRasterBand(3)

    # Create color bands and re-create color images
    red = band1.ReadAsArray()
    green = band2.ReadAsArray()
    blue = band3.ReadAsArray()
    rgbArray = np.dstack((red, green, blue))  # combine channels to get color image
    img = Image.fromarray(rgbArray)  # Now we have color image
    img.show("Original Image")

    return img

# Optional, but good for testing your model. Crop large image into a smaller one to test on.
def crop_image_to_new_size(image, y, new_height, x, new_width):
    img_array = np.asarray(image)
    crop_img = img_array[y: y + new_height, x: x + new_width]  # NOTE: its img[y: y + h, x: x + w] and *not* img[x: x + w, y: y + h]

    img = Image.fromarray(crop_img)  # Now we have cropped image
    img.show("Cropped Detect Houses", img)
    return img
