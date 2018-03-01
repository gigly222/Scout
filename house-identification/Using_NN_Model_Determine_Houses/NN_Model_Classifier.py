# How to load and use weights from a checkpoint
from keras.layers import Dropout, Flatten, Dense, Conv2D, MaxPooling2D, Input
from keras.applications.vgg16 import VGG16
from keras import backend as K
from keras.models import Model
from Chunking_image import chunk_image
import numpy
from Convert_image import convert_image_to_color, crop_image_to_new_size
from keras.optimizers import SGD
import numpy as np
import sys, os


# check for enough arguments
if len(sys.argv) != 4:
    print("Need to provide path to jp2 image. (This is your test image! Make sure NN hasn't seen this one before!). You also need to provide the saved weights from your model!")
    print("You need to provide the path with the name in which you want to save your converted jp2 image as a tif image.")
    sys.exit(1)

# Path to test image. Will be in jp2 format. Need to change this away from hard coding.
path_to_jp2 = sys.argv[1]
model_weights = sys.argv[2]
path_to_save_tif = sys.argv[3]

# Need to check if paths actually exist
if os.path.exists(path_to_jp2) and os.path.exists(model_weights):

    # Crop Image to this dimension, this information used in sliding Window
    img_width, img_height = 50, 50  # same as the training image sizes.
    stepSize = 25

    # fix random seed for reproducibility
    numpy.random.seed(7)

    # Load in Image to test Sliding Window On. Will need to convert jp2 to tiff, then to to a color jpg
    source_img = convert_image_to_color(path_to_jp2, path_to_save_tif)

    # OPTIONAL: If you want to, you can crop the original image to a smaller size. Good for testing how well NN works.
    source_img = crop_image_to_new_size(source_img, 0, 1500, 1000, 2500)

    # Get image shape
    if K.image_data_format() == 'channels_first':
        input_shape = (3, img_width, img_height)
    else:
        input_shape = (img_width, img_height, 3)

    # Load VGG16 model
    input_tensor = Input(shape=(input_shape))
    base_model = VGG16(input_tensor=input_tensor, weights='imagenet', include_top=False)
    x = base_model.output

    # Add a fully-connected layer
    x = Flatten(name='flatten')(x)
    x = Dense(4096, activation='relu', name='fc1')(x) #4096 are the number of nodes in fully connected layer
    x = Dropout(0.5)(x)
    x = Dense(4096, activation='relu', name='fc2')(x)
    x = Dropout(0.5)(x)
    x = Dense(1, activation='sigmoid', name='predictions')(x)  # and a logistic layer -- here we have 2 classes

    # This is the base of the model
    model = Model(input=base_model.input, output=x)

    # load saved weights. Provide path to saved weights.
    print("loading Weights from Saved Model")
    model.load_weights(model_weights)

    # first: train only the top layers (which were randomly initialized)
    # i.e. freeze all convolutional InceptionV3 layers
    for layer in base_model.layers:
        layer.trainable = False

    # compile the model (should be done *after* setting layers to non-trainable)
    sgd = SGD(lr=0.01, decay=1e-6, momentum=0.8, nesterov=True)
    model.compile(optimizer=sgd, loss='binary_crossentropy',metrics=['accuracy'])
    print("Model Compiled!")

    # convert image to array for cropping
    img_array = np.asarray(source_img)

    # Call chunk images. Image will be chunked into peices by sliding window.
    # Each window will be feed into the model to predict if it is a house or not a house. Draw a box around houses and save to file
    chunk_image(img_array, stepSize, img_width, img_height, model)

else:
    print("Either your path to your .jp2 test image or your model weights path is not found.")
    sys.exit(1)








'''EX Paths:
path_to_jp2 = "/Users/ee9w/Documents/skyScout/Cornerstone Sample/ShapeFiles_Houses_Mass/Boston/Boston_Images/19TCG285860/19TCG285860.jp2"
model_weights = "/Users/ee9w/PycharmProjects/Simple_Keras/weights.best.5.hdf5"
path_to_save_tif = "/Users/ee9w/Documents/skyScout/Cornerstone Sample/ShapeFiles_Houses_Mass/Boston/Boston_Images/19TCG285860/19TCG285860.tif"
'''