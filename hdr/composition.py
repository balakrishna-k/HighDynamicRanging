from hdr import gamma as gc
from utility import imageutil as im


def algo1(g, image1, image2, a1, image3, a2):

    img1 = image1.ravel()
    img2 = image2.ravel()
    img3 = image3.ravel()

    print(img1.shape[0] == img2.shape[0] == img3.shape[0])

    return


def __preprocess__(image, g):
    orig_channels = im.split_channels(image)
    corrected_channels = gc.invert_gamma_of_image(image, g, im.split_channels)

    orig_channels_raveled = __ravel__(orig_channels)
    corrected_channels_raveled = __ravel__(corrected_channels)

    return orig_channels_raveled, corrected_channels_raveled


def __ravel__(channels):

    for i in range(0, 3):
        channels[i] = channels[i].ravel()

    return channels
