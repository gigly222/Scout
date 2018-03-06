from osgeo import gdal
import numpy as np

driver = gdal.GetDriverByName('GTiff')
filename = "/Users/ee9w/Documents/skyScout/Cornerstone Sample/02 - GeoTiff_single_frame_ortho/or_025.tif"  # path to raster

dataset = gdal.Open(filename)

proj = dataset.GetProjection()
print(proj)

band = dataset.GetRasterBand(1)

cols = dataset.RasterXSize
rows = dataset.RasterYSize

print("Rows: ", rows, " Columns : " , cols)

transform = dataset.GetGeoTransform()

xOrigin = transform[0]
yOrigin = transform[3]  # (Upper left pixel position x,y)
pixelWidth = transform[1]
pixelHeight = -transform[5]

print("X-orgin ",  xOrigin)
print("Y-origin " , yOrigin)
print("Pixel Width, Height : (", pixelWidth, "," , pixelHeight , ")")    #(0.0,0.0) at the top left corner of the top left pixel


# GDAL affine transform parameters, According to gdal documentation xoff/yoff are image left corner, a/e are pixel wight/height and b/d is rotation and is zero if image is north up.

xoff, a, b, yoff, d, e = dataset.GetGeoTransform()           #Xorigin, a, b,  yOrigin ,d ,e      (Pixel size is b and e)

def pixel2coord(x, y):
   """Returns global coordinates from pixel x, y coords"""
   xp = a * x + b * y + xoff
   yp = d * x + e * y + yoff
   return(xp, yp)


# Empty array to store converted coordinates
convertImage = []

for row in  range(0,rows):
    convertRow = []
    for col in  range(0,cols):
        x,y = pixel2coord(col,row)
        print((x,y))
        convertRow.append(tuple([x,y]))
    convertImage.append(convertRow)

convertedImage = np.asarray(convertImage)
print("Shape : " , convertedImage.shape)
print("ROW 0: ", convertedImage[0])
print("length of Row : ", convertedImage[0].shape)

# Figure out how to write to file as tif image



'''
gdalinfo or_025.tif 
Driver: GTiff/GeoTIFF
Files: or_025.tif
Size is 12434, 8555
Coordinate System is:
LOCAL_CS["NAD83 / Nebraska (ftUS)",
    GEOGCS["NAD83",
        DATUM["unknown",
            SPHEROID["unretrievable - using WGS84",6378137,298.257223563]],
        PRIMEM["Greenwich",0],
        UNIT["degree",0.0174532925199433]],
    AUTHORITY["EPSG","26852"],
    UNIT["US survey foot",0.3048006096012192,
        AUTHORITY["EPSG","9003"]]]
Origin = (2542537.500000000000000,375241.500000000000000)
Pixel Size = (0.150000000000000,-0.150000000000000)
Metadata:
  AREA_OR_POINT=Point
  TIFFTAG_RESOLUTIONUNIT=1 (unitless)
  TIFFTAG_SOFTWARE=Trimble Germany GmbH
  TIFFTAG_XRESOLUTION=1
  TIFFTAG_YRESOLUTION=1
Image Structure Metadata:
  INTERLEAVE=PIXEL
Corner Coordinates:
Upper Left  ( 2542537.500,  375241.500) 
Lower Left  ( 2542537.500,  373958.250) 
Upper Right ( 2544402.600,  375241.500) 
Lower Right ( 2544402.600,  373958.250) 
Center      ( 2543470.050,  374599.875) 
Band 1 Block=512x512 Type=Byte, ColorInterp=Red
Band 2 Block=512x512 Type=Byte, ColorInterp=Green
Band 3 Block=512x512 Type=Byte, ColorInterp=Blue
Band 4 Block=512x512 Type=Byte, ColorInterp=Undefined
'''