import cv2 as cv

def read(path):
    img = cv.imread(path)
    print(img)
    return img

def display(caption, image, time=0):
    # Displays image with caption, if time (ms) is specified then closes image after time elapses
    cv.imshow(caption, image)
    cv.waitKey(time)

def write(image_path, image):
    cv.imwrite(image_path, image)

def split_channels(img):
    # Returns numpy array containing the channels : [r,g,b]
    return cv.split(img)

def combine_channels(channels):
    # Returns merged image, assuming channels : [r,g,b]
    return cv.merge((channels[0], channels[1], channels[2]))


def get_center_region(img, window_size = 100):
    [height, width] = img.shape[0:2]

    center = [int(height/2), int(width/2)]
    upper_limit = center[0] - window_size
    lower_limit = center[0] + window_size

    left_limit = center[1] - window_size
    right_limit = center[1] + window_size

    return img[upper_limit:lower_limit, left_limit:right_limit]