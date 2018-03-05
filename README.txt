--README


Written in Python - 3.5.2 (~/anaconda3/bin/python)
You will need to install gdal. As I recall, certain things would only work with certain versions of gdal. I had to install two versions of gdal.
I installed on my anaconda environment gdal	2.1.0. However, I had to install gdal version 2.1.3 outside of anaconda. You will also need Tensorflow and Keras. 


First you will need a set of images with their associated shape files. Look for Boston images and Boston Shape files. 
(From MassGIS http://www.mass.gov/anf/research-and-tech/it-serv-and-support/application-serv/office-of-geographic-information-massgis/datalayers/colororthos2013.html)
Your Boston images end in .jp2, your shape files end in .shp


# This command converts .jp2 to .tif
# To get this to work, i made a seperate conda environment with python=2.7 and did conda install -c conda-forge gdal=2.1.3
1) run command from cmd on a given .jp2 image (Where 19TCG240845.jp2 is the image to be converted to 19TCG240845.tif):
 		gdal_translate -of GTiff -co COMPRESS=JPEG -co TILED=YES 19TCG240845.jp2 19TCG240845.tif


# This converts shapefiles to Boston Coordinate system,
2) Open program called Converting_Shape_Files. This program will translate the Boston shape files to the correct coordinate system
to match the boston.jp2 files


# This crops shape files to same size and location as .jp2 image. It also returns the crop as a raster.
3) Open program Cropping_Raster. This program will take translated shape files, crop them to the same size and location 
as the .jp2 image of interest and rasterize them. You want your .jp2 file and shape files to align and be the same size!


# This creates a labeled data set for you based off of a cropped raster image that matches the .jp2 image you pass in.
4) Open program SkyScout_Create_Roof_Folders. This program will create you data set! You will need to provide it a cropped 
raster tif that aligns with your .jp2 image. You will need to create a folder to put houses in, and not_houses in. The THRESHOLD
value can be adjusted for different splits. Such as "30" calls an image house if 30% of their pixels are house. You should adjust
with this number and see how it affects your data set.


# Once you have a labeled data set, this program samples it and creates you a training, validation, and test set.
5) Once you have your labeled folder, we can now open SkyScout_randomly_sample_house_files. You will need path to folder containing 
subdirectories. Such as path to folder called 'all_houses', and 'all_houses' contains subdirectories 'house' and 'not_house'.
This program will randomly sample and create you a training, validation set and test set from your images. None of these
folders will share the same images! The classes are even, as in 50% are house, 50% are not house.


# This will use a training, validation and test set to train a VGG16 model. Saves weights.
6) Now you have your training, validation and test set. You are ready to train your Neural Network! I used VGG16. You will need to make
sure you have the appropriate information installed on your computer to use VGG16. Open program called Simple_Keras.
Run Main_VGG16. You weights will be stored, for example, as : "weights.best.hdf5"


# Uses a VGG16 models saved weights and runs a sliding window over a .jp2 image it has never seen before to find the houses in it.
7) You have a trained Model. Lets get a new .jp2 image that the model has never seen before! Open program called 
Using_NN_Model_Determine_Houses. This new .jp2 image is your new test data. This program will convert it to a color jpeg and 
run a slidding window over it. For each window, of size 50x50, it will feed the window into the model. The model will predict
if it is a house or not_house. For all windows predicted as house, it will draw a rectangle over it. The final jpeg image
with rectangles drawn over where the model thinks a house exists will be written to disk. You can open and view your results.


### I would try getting many more images to create my data set, in the hundred thousands. It would be useful to adjust the threshold value to
 see if you can get better results with something like THRESHOLD = 45. 
