import numpy as np

from hdr import gamma as gc
from hdr import exposure as xp

from utility import constants as ct
from utility import imageutil as im

disp = ct.DISPLAY_PLOT
exposure_times = ct.EXPOSURE_TIMES

new_gamma_brightness, gamma_brightness, g, fits = gc.invert_gamma_correction(display=disp)

print(g)

new_test_brightness = gc.compute_real_brightness_of_image(gamma_brightness, g)

xp.generate_hdr_stack_histogram(file_name="Histograms2.png", display=disp)

image1 = im.read(ct.GAMMA_READ_PATH + "/DSC_0015.JPG")
img = np.power(image1, 1.62)

print(image1.dtype == np.uint8)
print(np.amax(image1))
print(img.dtype == np.float64)
print(np.amax(img))
