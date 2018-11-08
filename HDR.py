from matplotlib import pylab as plb

from hdr import compositions as cp
from hdr import exposure as xp
from hdr import gamma as gc


times = [1, 1.38, 2, 2.78, 4.17, 5.56, 17.86, 25.00, 62.5]

red_fit, blue_fit, green_fit, brightness = gc.learn_gamma_correction_parameters(times)

gc.plot_brightness_fit(brightness[2], times, green_fit)

plb.plot(brightness[0])
plb.ylabel('Blue Channel Brightness')
plb.show()

plb.plot(brightness[1])
plb.ylabel('Green Channel Brightness')
plb.show()

plb.plot(brightness[2])
plb.ylabel('Red Channel Brightness')
plb.show()
