from hdr import gamma as gc
from hdr import exposure as xp

from utility import constants as ct

DISPLAY = ct.DISPLAY_PLOT

g = gc.learn_gamma_parameters_and_plot(display=DISPLAY)

print(g)

xp.generate_hdr_stack_histogram(file_name="Histograms.png", gamma_params=g, display=DISPLAY)
