'''
Driver (Main) file.
'''

import numpy as np
from PIL import Image

import random
from tqdm import tqdm

import cv2
import matplotlib.pyplot as plt

import os
import sys
import psutil
import time

from simulate_and_save import *


if __name__ == '__main__':

    # ______________ STEP 1__________________
    # Generating the parasite and veins image and saving them as .tif in the data directiory (less than 500 kb)
    session = 1

    # Initialie the simulation for this session
    simulate = Simulate(size = (10000, 10000), visualize = False, sess_num = session)

    # Generate fake parasite and fake veins to simulate. This will save the parasite image by default as a compressed .tif file
    parasite = simulate.generate_fake_parasite()
    veins_all, veins_body = simulate.generate_fake_veins(has_cancer = True)

    # Calculate if the parasite has cancer or not
    overlap = simulate.calculate_overlap(parasite, veins_body)

    print("-------- PART 1 RESULTS ---------")

    if overlap > cfg.CANCER_THRESHOLD:
        print("!!!!The parasite", session, "has cancer. Saving the veins image.!!!!")
        simulate.sparse_save(veins_all)
    else:
        print("No cancer detected in the parasite", session)

    print("Overlap found to be", overlap)

    print("__________________________________________________________________________________________")
    
    # Deleting the object to free space 
    del simulate

    # _______________STEP 2____________________
    # Importing the saved image, decompressing it, and findind if the parasite has cancer or not

    session = 2

    simulate = Simulate(size = (10000, 10000), visualize = False, sess_num = session)

    parasite = simulate.generate_fake_parasite()
    veins_all, veins_body = simulate.generate_fake_veins(has_cancer = False)

    overlap = simulate.calculate_overlap(parasite, veins_body)

    print("-------- PART 2 RESULTS ---------")

    if overlap > cfg.CANCER_THRESHOLD:
        print("!!!!The parasite", session, "has cancer. Saving the veins image.!!!!")
        simulate.sparse_save(veins_all)
    else:
        print("No cancer detected in the parasite", session)

    print("Overlap found to be", overlap)
    print("__________________________________________________________________________________________")

    del simulate