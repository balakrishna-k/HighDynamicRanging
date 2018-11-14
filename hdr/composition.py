import numpy as np

from hdr import gamma as gc

from utility import imageutil as im


def best_pixel_hdr(g, images, exposure_times):
    return generate_hdr(g, images, exposure_times, get_brightness_value_best)


def average_pixel_hdr(g, images, exposure_times):
    return generate_hdr(g, images, exposure_times, get_brightness_value_average)


def generate_hdr(g, images, exposure_times, callback):
    # 1. Compose Blue Channel of HDR - We need picture 1, 2 and 3's blue channels
    # 2. Compose Green Channel of HDR - We need picture 1, 2 and 3's green channels
    # 3. Compose Red Channel of HDR - We need picture 1, 2 and 3's red channels
    # 4. Combine Channels

    image1 = images[0]
    image2 = images[1]
    image3 = images[2]

    shp = image1.shape

    shp = shp[0: 2]

    a1 = exposure_times[1] / exposure_times[0]
    a2 = exposure_times[2] / exposure_times[0]

    a = [1, a1, a2]

    img1_channels, img1_corr_channels = __preprocess__(image1, g)
    img2_channels, img2_corr_channels = __preprocess__(image2, g)
    img3_channels, img3_corr_channels = __preprocess__(image3, g)

    image_channels = [img1_channels, img2_channels, img3_channels]
    corr_channels = [img1_corr_channels, img2_corr_channels, img3_corr_channels]

    blue_channels, corr_blue_channels = __get_channels_for_composition__(image_channels, corr_channels, 0)
    green_channels, corr_green_channels = __get_channels_for_composition__(image_channels, corr_channels, 1)
    red_channels, corr_red_channels = __get_channels_for_composition__(image_channels, corr_channels, 2)

    new_blue_channel = __compose_channels__(blue_channels, corr_blue_channels, a, g[0], callback)
    new_green_channel = __compose_channels__(green_channels, corr_green_channels, a, g[1], callback)
    new_red_channel = __compose_channels__(red_channels, corr_red_channels, a, g[2], callback)

    new_blue_channel = new_blue_channel.reshape(shp)
    new_green_channel = new_green_channel.reshape(shp)
    new_red_channel = new_red_channel.reshape(shp)

    new_blue_channel = np.power(new_blue_channel, 1/g[0])
    new_green_channel = np.power(new_green_channel, 1/g[1])
    new_red_channel = np.power(new_red_channel, 1/g[2])

    HDR_image = im.combine_channels([new_blue_channel, new_green_channel, new_red_channel])

    return HDR_image


def __compose_channels__(channels_pixels, corr_values, a, g, callback):
    # For a particular channel,
    # Returns a float64 image of channel
    new_channel_brightness = []

    for i in range(0, len(channels_pixels[0])):

        pixel1 = channels_pixels[0][i]
        pixel2 = channels_pixels[1][i]
        pixel3 = channels_pixels[2][i]

        brightness = [corr_values[0][i], corr_values[1][i], corr_values[2][i]]

        new_channel_brightness.append(callback(pixel1, pixel2, pixel3, brightness, a, g))

    return np.array(new_channel_brightness)


def get_brightness_value_best(pixel_1, pixel_2, pixel_3, corr_pixel_values, a, g):

    if pixel_3 <= 255 / a[2]:
        return corr_pixel_values[2] / a[2]
    elif pixel_2 <= 255 / a[1]:
        return corr_pixel_values[1] / a[1]
    else:
        return corr_pixel_values[0] / a[0]


def get_brightness_value_average(pixel_1, pixel_2, pixel_3, corr_pixel_values, a, g):
    if pixel_3 <= 255 / a[2]:
        return (corr_pixel_values[2] / a[2] + corr_pixel_values[1] / a[1] + corr_pixel_values[0] / a[0]) / 3
    elif pixel_2 <= 255 / a[1]:
        return (corr_pixel_values[1] / a[1] + corr_pixel_values[0] / a[0]) / 2
    else:
        return corr_pixel_values[0] / a[0]



def __get_channels_for_composition__(image_channels, corr_channels, channel):
    return [image_channels[0][channel], image_channels[1][channel], image_channels[2][channel]],\
           [corr_channels[0][channel], corr_channels[1][channel], corr_channels[2][channel]]


def __preprocess__(image, g):
    orig_channels = im.split_channels(image)
    corrected_channels = gc.invert_gamma_of_image(image, g, im.split_channels)

    orig_channels_raveled = __ravel__(orig_channels)
    corrected_channels_raveled = __ravel__(corrected_channels)

    return orig_channels_raveled, corrected_channels_raveled


def __ravel__(channels):
    # For an image's channels, converts them into 1D arrays
    new_channels = []
    # print(len(channels[2]))

    for i in range(0, 3):
        # print(i)
        new_channels.append(channels[i].ravel())

    return np.array(new_channels)


