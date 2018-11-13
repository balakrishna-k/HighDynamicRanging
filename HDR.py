from hdr import gamma as gc
from hdr import exposure as xp
from hdr import composition as cp

from utility import constants as ct

DISPLAY = ct.DISPLAY_PLOT

g = gc.learn_gamma_parameters_and_plot(display=DISPLAY)

print(g)

images = xp.generate_hdr_stack_histogram(file_name="Histograms.png", gamma_params=g, display=DISPLAY)

cp.algo1(g, images[0], images[1], 1, images[2], 2)


