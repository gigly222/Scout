''' Create a raster image where the shape files (representing houses) are white and all other pixels are black.'''
from osgeo import gdal, ogr, osr
import os, sys

# check for enough arguments
if len(sys.argv) != 4:
    print("Need input Tif image file, and shape file to rasterize, and file name the raster Tif image will be saved as...")
    sys.exit(1)

# Read in image Tif file
image_File = sys.argv[1]
# Read in Shapefile to rasterize. (The shape file that has been transformed to desired coordinate system)
vector_fn = sys.argv[2]
# Filename of the raster Tif that will be created and saved to disk
raster_fn = sys.argv[3]

# check if paths exists for Image Tif and Shape files. The path raster_fn will not exist yet.
if (os.path.exists(image_File)) and os.path.exists(vector_fn):

    dataset = gdal.Open(image_File)
    image_proj = dataset.GetProjection()
    band = dataset.GetRasterBand(1)

    # Get lrx, lry which is the lower right corner. These are used to crop the shape file to be the same size as the tif image of interest.
    xOrigin, pixelWidth, xskew, yOrigin, yskew, pixelHeight = dataset.GetGeoTransform()
    lrx = xOrigin + (dataset.RasterXSize * pixelWidth)
    lry = yOrigin + (dataset.RasterYSize * pixelHeight)

    # Tif Image Data
    print("lrx " , lrx)
    print("lry " , lry)
    print("X-orgin ",  xOrigin)
    print("Y-origin " , yOrigin)
    print("Pixel Width, Height : (", pixelWidth, ",", pixelHeight, ")")   # (0.0,0.0) at the top left corner of the top left pixel

    # Define pixel_size and NoData value of new raster
    NoData_value = -9999

    # Open the data source and read in the extent
    source_ds = ogr.Open(vector_fn)
    source_layer = source_ds.GetLayer()

    # Width and height of created raster in pixels, using Image file tif data
    x_wid = int((lrx- xOrigin)/pixelWidth)
    y_hig = int((yOrigin- lry)/(-pixelHeight))

    # The 1 means 1 band
    target_ds = gdal.GetDriverByName('GTiff').Create(raster_fn, x_wid, y_hig, 1, gdal.GDT_Byte)  # image file tiff
    target_ds.SetGeoTransform((xOrigin, pixelWidth, 0, yOrigin, 0, pixelHeight))

    utm29 = osr.SpatialReference()
    utm29.ImportFromEPSG(26919)
    target_ds.SetProjection(utm29.ExportToWkt())

    band = target_ds.GetRasterBand(1)
    band.SetNoDataValue(NoData_value)

    # Rasterize. Save a raster image that is the same size of the image of interest. Should be black and white!
    gdal.RasterizeLayer(target_ds, [1], source_layer, burn_values=[255])  # Want Houses to be white. House = 255 (white), NAN = 0 (black)

else:
    print("Either the input Tif image path or shape file to rasterize does not exist!")
    sys.exit(1)










''' EX paths
    # Read in image tif file
    image_File = "/Users/ee9w/Documents/skyScout/Cornerstone Sample/ShapeFiles_Houses_Mass/Boston/Boston_Images/19TCG240845/19TCG240845.tif"
    # Read in Shapefile to rasterize
    vector_fn = "/Users/ee9w/Documents/skyScout/Cornerstone Sample/ShapeFiles_Houses_Mass/Boston/Boston_ShapeFile/structures_poly_35/structures_poly_35_Trans.shp"
    # Filename of the raster Tiff that will be created and saved to disk
    raster_fn = "/Users/ee9w/Documents/skyScout/Cornerstone Sample/ShapeFiles_Houses_Mass/Boston/Boston_ShapeFile/structures_poly_35/poly_35_Raster_cropped_19TCG240845.tif"
'''