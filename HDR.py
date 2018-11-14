import numpy as np

import cv2

from hdr import gamma as gc
from hdr import exposure as xp
from hdr import composition as cp

from utility import constants as ct

DISPLAY = ct.DISPLAY_PLOT

g = gc.learn_gamma_parameters_and_plot(display=DISPLAY)

print(g)

images = xp.generate_hdr_stack_histogram(file_name="Histograms.png", file_name_exp="Histograms-exp.png", gamma_params=g, display=DISPLAY)

HDR = cp.average_pixel_hdr(g, images, ct.EXPOSURE_TIMES)

HDR = np.float32(HDR / 255)

tonemapReinhard = cv2.createTonemapReinhard(1.5, 0, 0, 0)
ldrReinhard = tonemapReinhard.process(HDR)
cv2.imwrite("ldr-Reinhard.jpg", ldrReinhard * 255)
