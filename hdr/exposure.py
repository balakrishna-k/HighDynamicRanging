from matplotlib import pyplot as plt

from utility import imageutil as im
from utility import constants as ct

plt.rc('font', size=ct.SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=ct.SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=ct.MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=ct.SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=ct.SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=ct.SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=ct.BIGGER_SIZE)  # fontsize of the figure title


def generate_hdr_stack_histogram(file_name, display=ct.DONT_DISPLAY_PLOT):
    image1 = im.read(ct.GAMMA_READ_PATH + "/DSC_0015.JPG")
    image2 = im.read(ct.GAMMA_READ_PATH + "/DSC_0017.JPG")
    image3 = im.read(ct.GAMMA_READ_PATH + "/DSC_0019.JPG")

    images = [image1, image2, image3]

    generate_histogram_mplt(file_name, images, display)


def generate_histogram_cv2(file_name, images, display=ct.DONT_DISPLAY_PLOT):
    graph_num = 0
    for i, image in enumerate(images):
        for j in range(0, 3):
            graph_num = graph_num + 1
            plt.subplot(int("33" + str(graph_num)))
            hist = im.histogram(image, j)
            plt.plot(hist, color=ct.CHANNEL_COLOUR[j])
            plt.title(ct.CHANNEL[j] + " Channel  \nPicture " + str(i + 1))

    plt.tight_layout()
    plt.savefig(ct.EXPOSURE_WRITE_PATH + "/" + file_name)

    if display is True:
        plt.show()


def generate_histogram_mplt(file_name, images, display=ct.DONT_DISPLAY_PLOT):
    graph_num = 0
    for idx, image in enumerate(images):
        channels = im.split_channels(image)

        for i in range(0, 3):
            channel = channels[i].ravel()
            graph_num = graph_num + 1
            plt.subplot(int("33" + str(graph_num)))
            plt.hist(channel, color=ct.CHANNEL_COLOUR[i], histtype='step')
            plt.title("Picture " + str(idx + 1))

    plt.tight_layout()
    plt.savefig(ct.EXPOSURE_WRITE_PATH + "/" + file_name)
    if display is True:
        plt.show()
