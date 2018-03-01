# Import Modules
import ogr, osr, os, sys

# Converts shape files into specified coordinate system. Must provide original coordinate sys and new coordinate sys.
def convert_cords(infile, outfile):

    # get path and filename seperately
    (out_file_path, out_file_name) = os.path.split(outfile)

    # get file name without extension
    (out_file_short_name, extension) = os.path.splitext(out_file_name)  # get file name without extension

    # Spatial Reference of the input file. (Need to look at the image to see what coordinate system it is in)
    # Access the Spatial Reference and assign the input projection
    in_SpatialRef = osr.SpatialReference()
    in_SpatialRef.ImportFromEPSG(26986)

    # Spatial Reference of the output file
    # Access the Spatial Reference and assign the output projection (Need to look up the output coordinate system you want)
    out_SpatialRef = osr.SpatialReference()
    out_SpatialRef.ImportFromEPSG(26919)

    # create Coordinate Transformation
    coordTransform = osr.CoordinateTransformation(in_SpatialRef, out_SpatialRef)

    # Open the input shapefile and get the layer
    driver = ogr.GetDriverByName('ESRI Shapefile')
    in_dataset = driver.Open(infile, 0)

    if in_dataset is None:
        print(' Could not open file')
        sys.exit(1)
    
    inlayer = in_dataset.GetLayer()

    # Create the output shapefile but check first if file exists
    if os.path.exists(outfile):
        driver.DeleteDataSource(outfile)

    out_dataset = driver.CreateDataSource(outfile)

    if outfile is None:
        print('Could not create file')
        sys.exit(1)
    out_layer = out_dataset.CreateLayer(out_file_short_name, geom_type=ogr.wkbPolygon)

    # Get the FieldDefn for attributes and add to output shapefile
    feature = inlayer.GetFeature(0)
    feild_array = []
    feild_name_array = []
    for i in range(feature.GetFieldCount()):
        name_of_feature = feature.GetDefnRef().GetFieldDefn(i).GetName()
        #print(name_of_feature)
        feild_name_array.append(name_of_feature)  # Gets list of all feature names
        feild_array.append(feature.GetDefnRef().GetFieldDefn(i))  # Now we have all feature names for all attributes

    for i in range(len(feild_array)):
        #print(type(featureArray[i]))
        out_layer.CreateField(feild_array[i])

    # get the FeatureDefn for the output shapefile
    feature_defn = out_layer.GetLayerDefn()

    # Loop through input features and write to output file
    in_feature = inlayer.GetNextFeature()
    while in_feature:
        # get the input geometry
        geometry = in_feature.GetGeometryRef()

        # re-project the geometry, each one has to be projected separately
        geometry.Transform(coordTransform)

        # create a new output feature
        out_feature = ogr.Feature(feature_defn)

        # set the geometry and attribute
        out_feature.SetGeometry(geometry)

        # Get features
        for i in range(len(feild_name_array)):
            out_feature.SetField(feild_name_array[i], in_feature.GetField(feild_name_array[i]))

        out_layer.CreateFeature(out_feature)

        # destroy the features and get the next input features
        out_feature.Destroy
        in_feature.Destroy
        in_feature = inlayer.GetNextFeature()

    # close the shapefiles
    in_dataset.Destroy()
    out_dataset.Destroy()

    # create the prj projection file
    out_SpatialRef.MorphToESRI()
    file = open(out_file_path + '/' + out_file_short_name + '.prj', 'w')

    file.write(out_SpatialRef.ExportToWkt())
    file.close()


