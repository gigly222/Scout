# Will convert shape files to specific coordinate system. For example, you want your shape files in the same coordinate system as an certain image.
from ConversionMethods import convert_cords
import sys
import os

if __name__ == "__main__":

    # check for enough arguments
    if len(sys.argv) != 3:
        print("Need input shape file path and the output path you want filed stored as...")
        sys.exit(1)

    # Get shapefile path and output path
    input_path=sys.argv[1]
    output_path=sys.argv[2]

    # check if path exists
    if os.path.exists(input_path) and os.path.exists(output_path):
        # Convert shape file to new coordinate system.
        print("Converting shape files to new coordinate system...")
        convert_cords(input_path, output_path)
    else:
        print("Either the input path or the output path does not exist!")
        sys.exit(1)










#EX Paths:
#input_path = "/Users/ee9w/Documents/skyScout/Cornerstone Sample/ShapeFiles_Houses_Mass/Boston/Boston_ShapeFile/structures_poly_35/structures_poly_35.shp" # shape files read in
#output_path = "/Users/ee9w/Documents/skyScout/Cornerstone Sample/ShapeFiles_Houses_Mass/Boston/Boston_ShapeFile/structures_poly_35/structures_poly_35_Trans.shp" # Transformed shape files out
