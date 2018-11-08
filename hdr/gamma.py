import numpy as np
from matplotlib import pylab as plb

from utility import imageutil as im
from utility import constants as ct
from utility import util as ut


def learn_gamma_correction_parameters(exp_times):
    images = im.load_images_from_folder(ct.GAMMA_READ_PATH, im.get_center_region)
    [b_brightness, g_brightness, r_brightness] = im.get_average_brightness_of_images(images)

    b_brightness = ut.sort_and_reshape_to_1D(b_brightness)
    g_brightness = ut.sort_and_reshape_to_1D(g_brightness)
    r_brightness = ut.sort_and_reshape_to_1D(r_brightness)

    b_fit = __curve_fit(b_brightness, exp_times)
    g_fit = __curve_fit(g_brightness, exp_times)
    r_fit = __curve_fit(r_brightness, exp_times)

    return b_fit, g_fit, r_fit, [b_brightness, g_brightness, r_brightness]


def invert_gamma_correction():
    return

def plot_brightness_fit(channel_brightness, exp_times, fit):
    plb.plot(channel_brightness, exp_times, 'o', color='k')
    plb.plot(channel_brightness, fit(channel_brightness), color='r')
    plb.xlabel('Exposure Time')
    plb.ylabel('Brightness $\mathrm{(B^{g})}$')
    plb.show()


def __curve_fit(channel_brightness, exp_times):
    poly = np.polynomial.Polynomial
    c_min, c_max = min(channel_brightness), max(channel_brightness)
    fit = poly.fit(channel_brightness, exp_times, 1, full=False, window=(c_min, c_max), domain=(c_min, c_max))

    return fit
