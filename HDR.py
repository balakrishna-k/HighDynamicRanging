from hdr import gamma as gc

from utility import constants as ct
from utility import imageutil as im

exposure_times = ct.EXPOSURE_TIMES

new_gamma_brightness, gamma_brightness, g, fits = gc.invert_gamma_correction(display=True)

print(g)

new_test_brightness = gc.compute_real_brightness_of_image(gamma_brightness, g)

images = im.load_images_from_folder(ct.GAMMA_READ_PATH)
