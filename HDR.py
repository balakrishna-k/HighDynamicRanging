from hdr import gamma as gc

from utility import constants as ct

exposure_times = ct.EXPOSURE_TIMES

new_gamma_brightness, gamma_brightness, g, fits = gc.invert_gamma_correction(exposure_times, display=True)

print(g)

new_test_brightness = gc.compute_real_brightness_of_image(gamma_brightness, g)
