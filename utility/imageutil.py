import cv2 as cv
import numpy as np
from utility import constants as ct
import os


def read(path):
    return cv.imread(path, 1)


def display(caption, image, time=ct.WAIT_FOR_KEY_PRESS):
    # Displays image with caption, if time (ms) is specified then closes image after time elapses
    cv.imshow(caption, image)
    cv.waitKey(time)


def write(image_path, image):
    cv.imwrite(image_path, image)


def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv.imread(os.path.join(folder, filename))
        if img is not None:
            images.append(img)
    return images


def split_channels(img):
    # Returns numpy array containing the channels : [b,g,r]
    return cv.split(img)


def combine_channels(channels):
    # Returns merged image, assuming channels : [b,g,r]
    return cv.merge((channels[0], channels[1], channels[2]))


def get_center_region(img, window_size=100):
    [height, width] = img.shape[0:2]

    center = [int(height / 2), int(width / 2)]
    upper_limit = center[0] - window_size
    lower_limit = center[0] + window_size

    left_limit = center[1] - window_size
    right_limit = center[1] + window_size

    return img[upper_limit:lower_limit, left_limit:right_limit]


def get_average_brightness(image):
    channels = split_channels(image)

    blue_brightness = get_average_brightness_of_channel(channels[0])
    green_brightness = get_average_brightness_of_channel(channels[1])
    red_brightness = get_average_brightness_of_channel(channels[2])

    return [blue_brightness, green_brightness, red_brightness]


def get_average_brightness_of_channel(channel):
    average_brightness = (np.sum(channel)) / channel.size
    return average_brightness
