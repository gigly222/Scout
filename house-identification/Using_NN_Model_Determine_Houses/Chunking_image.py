import cv2
import numpy as np

# Sliding window method. Slide window over image.
def sliding_window(image, stepSize, windowSize):
    # Slide a window across the image
    for y in range(0, image.shape[0], stepSize):
        for x in range(0, image.shape[1], stepSize):
            # yield the current window
            yield (x, y, image[y:y + windowSize[1], x:x + windowSize[0]])


# Chunking image into peices. For each chunk, classify if it is a house or not.
def chunk_image(image, stepSize, winW, winH, model):
    # loop over as sliding window over color image. Each cropped image we check # of shape file white pixels.
    for (x, y, window) in sliding_window(image, stepSize=stepSize, windowSize=(winW, winH)):
        # if the window does not meet our desired window size, ignore it
        if window.shape[0] != winH or window.shape[1] != winW:
            continue
        # Copy and crop images
        cloneImage = image.copy()
        crop_img = cloneImage[y: y + winH, x: x + winW]  # NOTE: its img[y: y + h, x: x + w] and *not* img[x: x + w, y: y + h]
        # Predict window as house or not house
        predict_if_house(model, crop_img, image, x, y, winW, winH)


# Draw Rectangle on Predicted Houses. Save image with boxes drawn on it to disk.
def predict_if_house(model, crop_img, source_img, x, y, winW, winH):
    # Trained model in batches. Need to make 4 dimensions, first being a batch size of 0
    exp_crop = np.expand_dims(crop_img, axis=0)
    pred = model.predict(exp_crop)
    rounded_num = round(pred[0][0]) # round probabilities to 0 or 1.
    if rounded_num == 0: # house, create box (0 == house)(1 == not house)
        cv2.rectangle(source_img, (x, y), (x + winW, y + winH), (255, 0, 0), 2)
        cv2.imwrite("house_detection_5.png", source_img)
