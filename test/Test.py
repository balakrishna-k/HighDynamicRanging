from utility import util as ut
from utility import imageutil as im

test_write_path = 'images/test/out'
test_read_path = 'images/test'

image = im.read('images/test/lenacolor.jpg')
image = im.read(ut.join_path(test_read_path, 'lenacolor.jpg'))

im.display("Lena", image)

[red_channel, green_channel, blue_channel] = im.split_channels(image)

im.display("Red Channel", red_channel, 1000)
im.display("Green Channel", green_channel, 1000)
im.display("Blue Channel", blue_channel, 1000)

center_image = im.get_center_region(image)
im.display("Region of Interest", center_image)

im.write(ut.join_path(test_write_path, 'lena_roi.png'), center_image)