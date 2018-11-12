import numpy as np

from matplotlib import pylab as plb

# from hdr import compositions as cp
# from hdr import exposure as xp
from hdr import gamma as gc

from utility import constants as ct

exposure_times = [1/30, 1/45, 1/60, 1/90, 1/125, 1/180, 1/250, 1/350, 1/500, 1/750, 1/1000, 1/1500, 1/2000, 1/3000]
exposure_times.reverse()
log_exp_times = np.log(exposure_times)

g_blue, g_green, g_red, fits, brightness = gc.learn_gamma_correction_parameters(log_exp_times)

gc.plot_brightness_of_channels(1, "ChannelBrightness.png", log_exp_times, brightness, np.exp)
gc.plot_brightness_fit(2, log_exp_times, brightness, fits)

print(g_blue, g_green, g_red)

brightness = np.exp(brightness)

blue_corrected = np.power(brightness[0], g_blue)
green_corrected = np.power(brightness[1], g_green)
red_corrected = np.power(brightness[2], g_green)

new_brightness = [blue_corrected, green_corrected, red_corrected]

gc.plot_brightness_of_channels(3, "CorrectedBrightness.png", exposure_times, new_brightness)

