import numpy as np

import cv2

from hdr import gamma as gc
from hdr import exposure as xp
from hdr import composition as cp

from utility import constants as ct

DISPLAY = ct.DISPLAY_PLOT
composite_images = []

# ------------------------------------------------------------------
# Learn Gamma Parameters for Camera
g = gc.learn_gamma_parameters_and_plot(display=DISPLAY)


# ------------------------------------------------------------------
# Generate Histograms for Picture Stack
images = xp.generate_hdr_stack_histogram(file_name="Histograms.png", file_name_exp="Histograms-exp.png",
                                         gamma_params=g, display=DISPLAY)


# ------------------------------------------------------------------
# Get Composite by Average
HDR = cp.average_pixel_hdr(g, images, ct.EXPOSURE_TIMES)
composite_images.append(HDR)
HDR = np.float32(HDR / 255)
# Using Reinhard Tone-map
tonemapReinhard = cv2.createTonemapReinhard(0.8, 0, 0, 0)
ldrReinhard = tonemapReinhard.process(HDR)
cv2.imwrite(ct.HDR_WRITE_PATH + "/HDR-average.jpg", ldrReinhard * 255)


# ------------------------------------------------------------------
# Get Composite by Pixel value/saturation
HDR = cp.best_pixel_hdr(g, images, ct.EXPOSURE_TIMES)
composite_images.append(HDR)
HDR = np.float32(HDR / 255)
# Using Reinhard Tone-map
tonemapReinhard = cv2.createTonemapReinhard(0.8, 0, 0, 0)
ldrReinhard = tonemapReinhard.process(HDR)
cv2.imwrite(ct.HDR_WRITE_PATH + "/HDR-best.jpg", ldrReinhard * 255)


# ------------------------------------------------------------------
# Generate Histograms for Composite
xp.__generate_composite_histogram__(composite_images, display=DISPLAY)