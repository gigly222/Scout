'''First run on jp2 image : gdal_translate -of GTiff -co COMPRESS=JPEG -co TILED=YES 19TCG240845.jp2 19TCG240845.tif
Convert shape file to correct coordinate system (ConvertingShapeFiles) (Really only need to do this once)
Run program that creates a raster that is same size as the jp2/tiff image. (CroppingRaster) Must crop shape file to same size as jp2!
In this program, we will take the cropped Raster and run a sliding window over it to chunk it into boxes.
Per box, we will determine if the pixels inside of it are above or below a certain threshold and use this to determine house or not house
In Summary: This program creates our dataset'''

from gdalconst import *
import numpy as np
import sys, os
from PIL import Image
from osgeo import gdal
import subprocess


# check for enough arguments
if len(sys.argv) != 6:
    print("Need both a path to folder you want to output houses to (positive) and a path to the folder you want to output negative (not_house) too.")
    print("You also need to provide a path to your cropped raster tif, this is the cropped shape file matching your image location and size.")
    print("You will need to provide a path to your .jp2 image which will be converted to a .tif file in this program.")
    print("Finally you will need to provide a path name in which you want your converted .jp2 file to be named and stored as.")
    sys.exit(1)

# Set Threshold Constant and paths (change to command line input)
THRESHOLD = 30  # This value determines what we consider a house. EX: 30% of pixels in box are white in the raster image, so we call it a house.
output_Path_Pos = sys.argv[1]
output_Path_Neg = sys.argv[2]
cropped_Raster_Tif = sys.argv[3]
boston_jp2_image = sys.argv[4]
path_convert_tif = sys.argv[5]

#Check to see if this path actually exists.
if (os.path.exists(output_Path_Pos)) and os.path.exists(output_Path_Neg) and os.path.exists(cropped_Raster_Tif) and os.path.exists(boston_jp2_image):

    #Read in Tif image (The raster of the jp2 of interest) This is a black and white image
    rasterTiffData = gdal.Open(cropped_Raster_Tif, GA_ReadOnly)
    rasterArray = np.array(rasterTiffData.ReadAsArray(), dtype=float)

    # Read in jp2 image, convert to tif file
    subprocess.call(['/Library/Frameworks/GDAL.framework/Programs/gdal_translate', '-of', 'GTiff', '-co', 'COMPRESS=JPEG', '-co' , 'TILED=YES', boston_jp2_image, path_convert_tif])

    # Read in convert jp2 which is now a tif image, using gdal
    dataset = gdal.Open(path_convert_tif)
    image_proj = dataset.GetProjection()
    band1 = dataset.GetRasterBand(1)  # split into RGB bands. Used to create color image.
    band2 = dataset.GetRasterBand(2)
    band3 = dataset.GetRasterBand(3)

    # Create color bands and re-create color images
    red = band1.ReadAsArray()
    green = band2.ReadAsArray()
    blue = band3.ReadAsArray()
    image = np.array(dataset.ReadAsArray(), dtype=float)
    rgbArray = np.dstack((red, green, blue)) # combine channels to get color image
    image = rgbArray # Now we have the color image

    # used fo cropping and naming images
    (winW, winH) = (50, 50) # window sizes
    count = 0 # used in naming cropped files

    # Sliding window of both jpg and tif raster image.
    def sliding_window(image, stepSize, windowSize):
        # slide a window across the image
        for y in range(0, image.shape[0], stepSize):
            for x in range(0, image.shape[1], stepSize):
                # yield the current window
                yield (x, y, image[y:y + windowSize[1], x:x + windowSize[0]])

    # loop over as sliding window over color image. Each cropped image we check # of shape file white pixels.
    for (x, y, window) in sliding_window(image, stepSize=25, windowSize=(winW, winH)):
        # if the window does not meet our desired window size, ignore it
        if window.shape[0] != winH or window.shape[1] != winW:
            continue

        # Copy and crop images and tiff file
        clone = rasterArray.copy()
        cloneImage = image.copy()
        crop_img_raster = clone[y: y + winH, x: x + winW]  # NOTE: its img[y: y + h, x: x + w] and *not* img[x: x + w, y: y + h]
        stringLine = str(count)+ 'crop.jpg'
        crop_img = cloneImage[y: y + winH, x: x + winW]  # NOTE: its img[y: y + h, x: x + w] and *not* img[x: x + w, y: y + h]

        # Find total white pixels (part of house) per cropped raster image on tiff in percentage
        totalPixels, totalWhitePixels = 0, 0
        for eachVal in crop_img_raster:
            for val in eachVal:
                if val == 255:
                    totalWhitePixels += 1
                totalPixels += 1
            sum = np.sum(eachVal)
        percentOfTotal = (totalWhitePixels/totalPixels) * 100;

        if percentOfTotal > THRESHOLD:  # Write cropped image to house file if # of shape file pixels above the threshold.
            img = Image.fromarray(crop_img)
            img.save(os.path.join(output_Path_Pos, stringLine))
        else:
            img = Image.fromarray(crop_img)
            img.save(os.path.join(output_Path_Neg, stringLine))

        count += 1

else:
    print("ERROR: Path to positive output folder, or path to negative output folder, or to your cropped raster image, or your path to your jp2 file is not found!")
    sys.exit(1)












'''Ex Paths:
outputPathPos = "/Users/ee9w/Documents/skyScout/Cornerstone Sample/ShapeFiles_Houses_Mass/Boston/19TCG240845_50_house"
outputPathNeg = "/Users/ee9w/Documents/skyScout/Cornerstone Sample/ShapeFiles_Houses_Mass/Boston/19TCG240845_50_not_house"
croppedRasterTif = ""/Users/ee9w/Documents/skyScout/Cornerstone Sample/ShapeFiles_Houses_Mass/Boston/Boston_ShapeFile/structures_poly_35/poly_35_Raster_cropped_19TCG240845.tif"
boston_jp2_image= '/Users/ee9w/Documents/skyScout/Cornerstone Sample/ShapeFiles_Houses_Mass/Boston/Boston_Images/19TCG240845/19TCG240845.jp2'
path_convert_tif, '/Users/ee9w/Documents/skyScout/Cornerstone Sample/ShapeFiles_Houses_Mass/Boston/Boston_Images/19TCG240845/19TCG240845.tif'
'''