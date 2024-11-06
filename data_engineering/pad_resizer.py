import os
import numpy as np
import cv2 as cv


def pad_resize(img, size):
    """generates an image with padded with (0,0,0) to the desired_size"""
    color = (0, 0, 0)
    if len(img.shape) == 3:
        old_image_height, old_image_width, channels = img.shape
        new_image_height, new_image_width = max(old_image_height, old_image_width), max(old_image_height, old_image_width)
        result = np.full((new_image_height, new_image_width, channels), color, dtype=np.uint8)
    else:
        old_image_height, old_image_width = img.shape
        new_image_height, new_image_width = max(old_image_height, old_image_width), max(old_image_height, old_image_width)
        result = np.full((new_image_height, new_image_width), 0, dtype=np.uint8)

    # create new image of desired size and color (black) for padding
    
    # compute center offset
    x_center = (new_image_width - old_image_width) // 2
    y_center = (new_image_height - old_image_height) // 2

    # copy img image into center of result image
    result[y_center:y_center+old_image_height, x_center:x_center+old_image_width] = img
    result = cv.resize(result, (size, size), interpolation=cv.INTER_LINEAR)
    return result

img_dir = '../segmentation/samples'
mask_dir = '../segmentation/masks'

for i in os.listdir(img_dir):
    img = cv.imread(os.path.join(img_dir, i), cv.IMREAD_COLOR)
    mask = cv.imread(os.path.join(mask_dir, i), cv.IMREAD_GRAYSCALE)
    img = pad_resize(img, 256)
    mask = pad_resize(mask, 256)

    cv.imwrite(os.path.join(img_dir, i), img)
    cv.imwrite(os.path.join(mask_dir, i), mask)



