import numpy as np

from matplotlib import pylab as plb

from utility import imageutil as im
from utility import constants as ct
from utility import util as ut


def learn_gamma_correction_parameters(exp_times):
    # Learns the gamma correction applied by the camera.
    # Reads images from the gamma correction images directory

    images = im.load_images_from_folder(ct.GAMMA_READ_PATH, im.get_center_region)
    # We consider the log of the brightness, so we pass the np.log to the function
    [b_brightness, g_brightness, r_brightness] = im.get_average_brightness_of_images(images, np.log)

    b_brightness = ut.sort_and_reshape_to_1D(b_brightness)
    g_brightness = ut.sort_and_reshape_to_1D(g_brightness)
    r_brightness = ut.sort_and_reshape_to_1D(r_brightness)

    b_fit = __curve_fit(exp_times, b_brightness)
    g_fit = __curve_fit(exp_times, g_brightness)
    r_fit = __curve_fit(exp_times, r_brightness)

    return b_fit, g_fit, r_fit, [b_brightness, g_brightness, r_brightness]


def invert_gamma_correction():
    return


def plot_brightness_fit(X, Y, fit):
    plb.plot(X, Y, 'o', color='k')
    plb.plot(X, fit(X), color='r')
    plb.xlabel('Exposure Time')
    plb.ylabel('Brightness $\mathrm{(B^{g})}$')
    plb.show()


def __curve_fit(X, Y):
    poly = np.polynomial.Polynomial
    c_min, c_max = min(Y), max(Y)
    fit = poly.fit(X, Y, 1, full=False, window=(c_min, c_max), domain=(c_min, c_max))

    return fit

# def learn_gamma_correction_parameters_v2(exp_times):
#     # Learns the gamma correction applied by the camera.
#     # Reads images from the gamma correction images directory
#
#     images = im.load_images_from_folder(ct.GAMMA_READ_PATH, im.get_center_region)
#     # We consider the log of the brightness, so we pass the np.log to the function
#     [b_brightness, g_brightness, r_brightness] = im.get_average_brightness_of_images(images, np.log)
#
#     b_brightness = ut.sort_and_reshape_to_1D(b_brightness)
#     g_brightness = ut.sort_and_reshape_to_1D(g_brightness)
#     r_brightness = ut.sort_and_reshape_to_1D(r_brightness)
#
#     b_pred = __curve_fit_v2(exp_times, b_brightness)
#     g_pred = __curve_fit_v2(exp_times, g_brightness)
#     r_pred = __curve_fit_v2(exp_times, r_brightness)
#
#     return b_pred, g_pred, r_pred, [b_brightness, g_brightness, r_brightness]
#

#
# def plot_brightness_fit_v2(X, Y, predictions):
#     plb.plot(X, Y, 'o', color='k')
#     plb.plot(X, predictions, color='r')
#     plb.xlabel('Exposure Time')
#     plb.ylabel('Brightness $\mathrm{(B^{g})}$')
#
#     plb.xticks(())
#     plb.yticks(())
#
#     plb.show()
#


# def __curve_fit_v2(X, Y):
#     X = X.reshape(X.shape[0], 1)
#     Y = Y.reshape(Y.shape[0], 1)
#     regr = linear_model.LinearRegression()
#
#     regr.fit(X, Y)
#
#     predictions = regr.predict(X)
#     print(regr.coef_)
#
#     return predictions
