import os

'''
Directory configurations
'''
DATA_DIR = "data"
PROCESSED_DIR = os.path.join(DATA_DIR, "body")
COLLECTED_DIR = os.path.join(DATA_DIR, "veins")

'''
Data Information
'''
INPUT_SIZE = 100000

MAX_ROWS = 100000
MAX_COLS = 100000

'''
Parasite configurations
'''
MIN_BODY_PERCENTAGE= 0.25
PARASITE_BORDER_BIAS = 6        # Higher the number, more centered the fake simulated parasite is
PARASITE_RADIUS_LOW = 0.45
PARASITE_RADIUS_HIGH = 0.55

'''
Veins configurations
'''
NUM_OF_VEIN_NODES = 4
NUM_OF_VEINS_PER_NODE = 10
SMALL_CANCER_STROKE = 50
SMALL_NO_CANCER_STROKE = 5
LARGE_CANCER_STROKE = 150
LARGE_NO_CANCER_STROKE = 15

'''
Cancer information
'''
CANCER_THRESHOLD = 0.10
SIM_CANCER_RATE = 0.001

'''
Visualization information
'''
MAX_SIZE_TO_DEBUG = 50001