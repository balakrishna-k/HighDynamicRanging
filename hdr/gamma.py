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

    c_b, m_b = b_fit
    c_g, m_g = g_fit
    c_r, m_r = r_fit

    g_b = 1 / m_b
    g_g = 1 / m_g
    g_r = 1 / m_r

    return g_b, g_g, g_r, [b_fit, g_fit, r_fit], [b_brightness, g_brightness, r_brightness]


def __curve_fit(X, Y):
    poly = np.polynomial.Polynomial
    c_min, c_max = min(Y), max(Y)
    fit = poly.fit(X, Y, 1, full=False, window=(c_min, c_max), domain=(c_min, c_max))

    return fit


def invert_gamma_correction(g_b, g_g, g_r):
    brightness = 0
    return brightness


def plot_brightness_of_channels(figure_number, file_name, X, Y, callback=None):
    plb.figure(figure_number)

    for i in range(0, 3):
        channel = Y[i]
        if callback is not None:
            channel = callback(Y[i])
            X = callback(X)
        plb.subplot(int("31" + str(i + 1)))
        plb.plot(X, channel)
        plb.ylabel(ct.CHANNEL[i] + ' Channel \n Brightness')
        plb.xlabel('Exposure Time - log(T)')

    plb.savefig(ct.GAMMA_WRITE_PATH + "/" + file_name)
    plb.show()


def plot_brightness_fit(figure_number, X, Y, fits):
    plb.figure(figure_number)

    for i in range(0, 3):
        channel_brightness = Y[i]
        fit = fits[i]
        plb.subplot(int("31" + str(i+1)))
        plb.plot(X, channel_brightness, 'o', color='k')
        plb.plot(X, fit(X), color='r')
        plb.xlabel('Exposure Time - log(T)')

        plb.ylabel(ct.CHANNEL[i] + ' Channel \n Brightness $\mathrm{(B^{g})}$')

    plb.savefig(ct.GAMMA_WRITE_PATH + "/LinearRegression.png")
    plb.show()


def plot_channel_brightness_fit(X, Y, fit):
    plb.plot(X, Y, 'o', color='k')
    plb.plot(X, fit(X), color='r')
    plb.xlabel('Exposure Time')
    plb.ylabel('Brightness $\mathrm{(B^{g})}$')
    plb.show()

