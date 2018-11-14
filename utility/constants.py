# -----------------------------------------------
# PLOT DISPLAY CONSTANTS
DONT_DISPLAY_PLOT = False
DISPLAY_PLOT = True

# -----------------------------------------------
# CHANNEL CONSTANTS
CHANNEL = {0: "Blue", 1: "Green", 2: "Red"}
CHANNEL_COLOUR = {0: 'b', 1: 'g', 2: 'r'}

# -----------------------------------------------
# GAMMA CORRECTION PARAMETERS
GAMMA_EXPOSURE_TIMES = [1 / 350, 1 / 250, 1 / 180, 1 / 125, 1 / 90, 1 / 60, 1 / 45, 1 / 30]

# -----------------------------------------------
# EXPOSURE PARAMETERS
# EXPOSURE_TIMES = [1 / 350, 1 / 90, 1 / 30]
EXPOSURE_TIMES = [1/ 1500, 1 / 350, 1 / 125]
# -----------------------------------------------
# IMAGE PATHS
GAMMA_WRITE_PATH = 'images/gamma/out'
GAMMA_READ_PATH = 'images/gamma'

EXPOSURE_WRITE_PATH = 'images/exposure/out'
EXPOSURE_READ_PATH = 'images/exposure'

HDR_WRITE_PATH = 'images/hdr/out'
HDR_READ_PATH = 'images/hdr'

TEST_WRITE_PATH = 'images/test/out'
TEST_READ_PATH = 'images/test'

# ----------------------------------------------
# IMAGE DISPLAY TIME CONSTANTS
IMAGE_DISPLAY_TIME = 1000
WAIT_FOR_KEY_PRESS = 0

# ----------------------------------------------
# MATPLOTLIB CONSTANTS
SMALL_SIZE = 8
MEDIUM_SIZE = 10
BIGGER_SIZE = 12

# ----------------------------------------------
# HISTOGRAM CONSTANTS
BIN_COUNT = 256
