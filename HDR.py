import numpy as np

from matplotlib import pylab as plb

# from hdr import compositions as cp
# from hdr import exposure as xp
from hdr import gamma as gc

exposure_times = [1/30, 1/45, 1/60, 1/90, 1/125, 1/180, 1/250, 1/350, 1/500, 1/750, 1/1000, 1/1500, 1/2000, 1/3000]
exposure_times.reverse()
log_exp_times = np.log(exposure_times)

red_fit, blue_fit, green_fit, brightness = gc.learn_gamma_correction_parameters(log_exp_times)

print(brightness[0])

plb.plot(np.log(exposure_times), brightness[0], 'o')
plb.ylabel('Blue Channel Brightness')
plb.show()

plb.plot(np.log(exposure_times), brightness[1], 'o')
plb.ylabel('Green Channel Brightness')
plb.show()

plb.plot(exposure_times, brightness[2], 'o')
plb.ylabel('Red Channel Brightness')
plb.show()

gc.plot_brightness_fit(log_exp_times, brightness[0], blue_fit)
gc.plot_brightness_fit(log_exp_times, brightness[1], green_fit)
gc.plot_brightness_fit(log_exp_times, brightness[2], red_fit)

c_blue, m_blue = blue_fit
c_green, m_green = green_fit
c_red, m_red = red_fit

g_blue = 1 / m_blue
g_green = 1 / m_green
g_red = 1 / m_red

print(g_blue, g_green, g_red)
