import numpy as np

from utility import util as ut
from utility import imageutil as im
from utility import constants as ct

test_write_path = ct.TEST_WRITE_PATH
test_read_path = ct.TEST_READ_PATH

image = im.read(ut.join_path(test_read_path, 'lena_color.jpg'))

im.display("Lena", image, ct.IMAGE_DISPLAY_TIME)

[blue_channel, green_channel, red_channel] = im.split_channels(image)

im.display("Blue Channel", blue_channel, ct.IMAGE_DISPLAY_TIME)
im.display("Green Channel", green_channel, ct.IMAGE_DISPLAY_TIME)
im.display("Red Channel", red_channel, ct.IMAGE_DISPLAY_TIME)

center_image = im.get_center_region(image)
im.display("Region of Interest", center_image)

im.write(ut.join_path(test_write_path, 'lena_roi.png'), center_image)

print(im.get_average_brightness(image))

images = im.load_images_from_folder(ct.GAMMA_READ_PATH)

matrix = [-1, -1, -1]
for image in images:
    matrix = np.vstack((im.get_average_brightness(image), matrix))


matrix = np.delete(matrix, matrix.shape[0]-1, 0)
# print(matrix)

blue_array = matrix[:, 0]
green_array = matrix[:, 1]
red_array = matrix[:, 2]

print(blue_array)
