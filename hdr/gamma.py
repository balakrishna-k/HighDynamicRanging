import numpy as np

from utility import imageutil as im
from utility import constants as ct

# images = im.load_images_from_folder(ct.GAMMA_READ_PATH)
# matrix = [-1, -1, -1]
# for image in images:
#     matrix = np.vstack((im.get_average_brightness(image), matrix))
#
#
# matrix = np.delete(matrix, matrix.shape[0]-1, 0)
# # print(matrix)
#
# blue_array = matrix[:, 0]
# green_array = matrix[:, 1]
# red_array = matrix[:, 2]
#
# print(blue_array)