import numpy as np

from matplotlib import pyplot as plb

from utility import imageutil as im
from utility import constants as ct
from utility import util as ut


def invert_gamma_of_image(image, gamma_params, callback=None):
    # requires parameter g, simply inverts gamma correction and returns new float64 image
    # Optional callback whose Intended use is to help in conversion from float64 to other formats (like float32) ONLY

    if gamma_params is None:
        raise RuntimeError("You must pass in a list of gamma parameters as [g_b, g_g, g_r]")
    channels = im.split_channels(image)
    corrected_channels = [np.power(channels[0], gamma_params[0]),
                          np.power(channels[1], gamma_params[1]),
                          np.power(channels[2], gamma_params[2])]
    new_image = im.combine_channels(corrected_channels)

    if callback is not None:
        new_image = callback(new_image)

    return new_image


def learn_gamma_parameters_and_plot(exp_times=ct.GAMMA_EXPOSURE_TIMES, display=ct.DONT_DISPLAY_PLOT):
    # If display is set to true, then popups of the plots are shown and written to the gamma output folder

    # Returns g parameters

    exp_times = np.log(exp_times)

    g_b, g_g, g_r, fits, orig_brightness, images = __learn_gamma_correction_parameters__(exp_times)
    g = [g_b, g_g, g_r]

    # Reversing log that was applied
    orig_brightness = np.exp(orig_brightness)
    corrected_images = []
    for image in images:
        channels = im.split_channels(image)
        corrected_channels = [np.power(channels[0], g_b), np.power(channels[1], g_g), np.power(channels[2], g_r)]
        corrected_images.append(im.combine_channels(corrected_channels))

    [b_brightness, g_brightness, r_brightness] = im.get_average_brightness_of_images(corrected_images)
    b_brightness = ut.sort_and_reshape_to_1D(b_brightness)
    g_brightness = ut.sort_and_reshape_to_1D(g_brightness)
    r_brightness = ut.sort_and_reshape_to_1D(r_brightness)

    new_brightness = [b_brightness, g_brightness, r_brightness]

    # new_brightness = compute_real_brightness_of_image(orig_brightness, g)

    __plot_brightness_of_channels__(1, "ChannelBrightness.png", "Channel Brightness v/s Exposure Time",
                                    np.exp(exp_times), orig_brightness, display=display)
    __plot_linear_fit__(2, "LinearRegression.png", "Linear Fit",
                        exp_times, np.log(orig_brightness), fits, display=display)
    __plot_brightness_of_channels__(3, "CorrectedBrightness.png", "Real Channel Brightness v/s Exposure Time",
                                    np.exp(exp_times), new_brightness, display=display)

    return g


def __learn_gamma_correction_parameters__(exp_times):
    # Learns the gamma correction applied by the camera.
    # Reads images from the gamma correction images directory

    images = im.load_images_from_folder(ct.GAMMA_READ_PATH, im.get_center_region)
    # We consider the log of the brightness, so we pass the np.log to the function
    [b_brightness, g_brightness, r_brightness] = im.get_average_brightness_of_images(images, np.log)

    b_brightness = ut.sort_and_reshape_to_1D(b_brightness)
    g_brightness = ut.sort_and_reshape_to_1D(g_brightness)
    r_brightness = ut.sort_and_reshape_to_1D(r_brightness)

    b_fit = __curve_fit__(exp_times, b_brightness)
    g_fit = __curve_fit__(exp_times, g_brightness)
    r_fit = __curve_fit__(exp_times, r_brightness)

    c_b, m_b = b_fit
    c_g, m_g = g_fit
    c_r, m_r = r_fit

    g_b = 1 / m_b
    g_g = 1 / m_g
    g_r = 1 / m_r

    return g_b, g_g, g_r, [b_fit, g_fit, r_fit], [b_brightness, g_brightness, r_brightness], images


def __curve_fit__(X, Y):
    poly = np.polynomial.Polynomial
    c_min, c_max = min(Y), max(Y)
    fit = poly.fit(X, Y, 1, full=False, window=(c_min, c_max), domain=(c_min, c_max))

    return fit


def __plot_brightness_of_channels__(figure_number, file_name, title, X, Y, callback=None, display=ct.DONT_DISPLAY_PLOT):
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

    if display is True:
        plb.show()


def __plot_linear_fit__(figure_number, file_name, title, X, Y, fits, display=ct.DONT_DISPLAY_PLOT):
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

    if display is True:
        plb.show()
