import numpy as np

from matplotlib import pylab as plb

from utility import imageutil as im
from utility import constants as ct
from utility import util as ut


def compute_real_brightness_of_image(orig_brightness, g):
    # Given parameter g, simply inverts gamma correction and returns new brightness

    blue_corrected = np.power(orig_brightness[0], g[0])
    green_corrected = np.power(orig_brightness[1], g[1])
    red_corrected = np.power(orig_brightness[2], g[2])

    new_brightness = [blue_corrected, green_corrected, red_corrected]

    return new_brightness


def invert_gamma_correction(exp_times=ct.EXPOSURE_TIMES, display=False):
    # If display is set to true, then popups of the plots are shown and written to the gamma output folder

    # Returns corrected brightness, original brightness, g parameters, polynomial fits

    exp_times = np.log(exp_times)

    g_b, g_g, g_r, fits, orig_brightness = learn_gamma_correction_parameters(exp_times)
    g = [g_b, g_g, g_r]

    # Reversing log that was applied
    orig_brightness = np.exp(orig_brightness)
    new_brightness = compute_real_brightness_of_image(orig_brightness, g)

    if display is True:
        plot_brightness_of_channels(1, "ChannelBrightness.png", "Channel Brightness v/s Exposure Time",
                                    np.exp(exp_times), orig_brightness)
        plot_linear_fit(2, "LinearRegression.png", "Linear Fit",
                        exp_times, np.log(orig_brightness), fits)
        plot_brightness_of_channels(3, "CorrectedBrightness.png", "Real Channel Brightness v/s Exposure Time",
                                    np.exp(exp_times), new_brightness)

    return new_brightness, orig_brightness, g, fits


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


def plot_brightness_of_channels(figure_number, file_name, title, X, Y, callback=None):
    plb.figure(figure_number)
    for i in range(0, 3):
        channel = Y[i]
        if callback is not None:
            channel = callback(Y[i])
            X = callback(X)
        plb.subplot(int("31" + str(i + 1)))
        plb.plot(X, channel, color=ct.CHANNEL_COLOUR[i])
        plb.ylabel(ct.CHANNEL[i] + ' Channel \n Brightness')
        plb.xlabel('Exposure Time - T')

    plb.tight_layout()
    plb.suptitle(title)
    plb.subplots_adjust(top=0.93)
    plb.savefig(ct.GAMMA_WRITE_PATH + "/" + file_name)
    plb.show()


def plot_linear_fit(figure_number, file_name, title, X, Y, fits):
    plb.figure(figure_number)

    for i in range(0, 3):
        channel_brightness = Y[i]
        fit = fits[i]
        plb.subplot(int("31" + str(i + 1)))
        plb.plot(X, channel_brightness, 'o', color='k')
        plb.plot(X, fit(X), color=ct.CHANNEL_COLOUR[i])
        plb.xlabel('Exposure Time - log(T)')

        plb.ylabel(ct.CHANNEL[i] + ' Channel \n Brightness $\mathrm{(B^{g})}$')

    plb.suptitle(title)
    plb.tight_layout()
    plb.subplots_adjust(top=0.93)
    plb.savefig(ct.GAMMA_WRITE_PATH + "/" + file_name)
    plb.show()
