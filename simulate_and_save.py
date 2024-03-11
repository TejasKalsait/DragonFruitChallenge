'''
This file contains the Simulate class which is responsible for generating fake parasite body and parasite veins images according to the config file parameters.
Every rule from DragonFruit.AI has been thought of and fulfilled.
'''

import config as cfg

import matplotlib.pyplot as plt
import numpy as np
import random
import cv2

from PIL import Image

from random import randint, choice
from skimage.transform import resize
from itertools import groupby
import pickle


import os
import sys

from tqdm import tqdm

'''

This class handles the creation of parasite and veins image, and compresses it using RLE and Sparse matrix techniques respectively.

'''

class Simulate():

    def __init__(self, size = (1000, 1000), visualize = False, sess_num = 1):
        
        self.size = size
        self.sess_num = sess_num

        self.parasite_img = None
        self.compressed_parasite_img = None
        self.compressed_veins_img = None

        self.parasite_area = None
        self.parasite_radius = None
        self.parasite_center = None
        self.veins_area = None

        self.visualize = visualize


    # Creates a parasite image with parasite occupying more than 25% of the image
    def generate_fake_parasite(self):
        
        # Storing dimensions
        height = min(self.size[0], cfg.MAX_ROWS)
        width = min(self.size[1], cfg.MAX_COLS)
 
        '''
        Generating parasite location and size at random to create a more realistic simulation.
        Making sure that the size remains >25% of the image
        '''
        
        # Generating center coordinates and radius for the fake parasite
        # the number 6 just works really well to make sure to stay away from the borders while generating fake parasites
        parasite_center_height = random.randint(int(height//cfg.PARASITE_BORDER_BIAS), height - int(height//cfg.PARASITE_BORDER_BIAS))
        parasite_center_width = random.randint(int(width//cfg.PARASITE_BORDER_BIAS), width - int(width//cfg.PARASITE_BORDER_BIAS))
        self.parasite_radius = int(random.uniform(cfg.PARASITE_RADIUS_LOW, cfg.PARASITE_RADIUS_HIGH) * height)
        self.parasite_center = (parasite_center_height, parasite_center_width)

        # Creating an image with a parasite in it
        self.compressed_parasite_img = np.full((height, width), 0, dtype=np.uint8)

        # Draw a circular Parasite
        cv2.circle(self.compressed_parasite_img, (parasite_center_width, parasite_center_height), self.parasite_radius, 1, thickness = -1)

        # Changing to bool values
        #self.compressed_parasite_img = self.compressed_parasite_img.astype(bool)

        # Calculating the area of the parasite
        self.parasite_area = np.sum(self.compressed_parasite_img)

        # Visualize the parasite
        if self.visualize and height < cfg.MAX_SIZE_TO_DEBUG:             # Don't Visualise if the dimensions are more than 50,000 because no sense in filing up the RAM
            plt.imshow(np.asarray(self.compressed_parasite_img), cmap = 'gray')
            print("Displaying the parasite with area", self.parasite_area)
            plt.show()

        print("Fake parasite generated.")
        #cv2.imwrite("uncompressed_image.jpg", self.compressed_parasite_img * 255)
        self.parasite_img = self.compressed_parasite_img

        return self._rle_compress(self.compressed_parasite_img, is_parasite = True)

    # Generates a veins image. has_cancer makes sure if we want to simulate a cancer parasite or non-cancer parasite
    def generate_fake_veins(self, has_cancer = False):

        # Storing dimensions
        height = min(self.size[0], cfg.MAX_ROWS)
        width = min(self.size[1], cfg.MAX_COLS)

        # If information not avalable... Generate it to avoid errora
        if not self.parasite_center:
            print("Center infomation not available. Generating...")
            parasite_center_height = random.randint(int(height//cfg.PARASITE_BORDER_BIAS), height)
            parasite_center_width = random.randint(int(width//cfg.PARASITE_BORDER_BIAS), width)
            self.parasite_radius = int(random.uniform(cfg.PARASITE_RADIUS_LOW, cfg.PARASITE_RADIUS_HIGH) * height)

        parasite_center_height, parasite_center_width = self.parasite_center
        veins_img = np.full((height, width), 0, dtype = np.uint8)


        # Generate starting points for the veins to expand from. Always including the center point
        veins_starting_points = [(parasite_center_width, parasite_center_height)]
        for i in range(cfg.NUM_OF_VEIN_NODES):
            random_x = random.randint(parasite_center_width - self.parasite_radius, parasite_center_height + self.parasite_radius)
            random_y = random.randint(parasite_center_width - self.parasite_radius, parasite_center_height + self.parasite_radius)
            veins_starting_points.append((random_x, random_y))

        # Drawing lines as veins
        for vein_node in veins_starting_points:

            start_x = vein_node[0]
            start_y = vein_node[1]

            for i in range(cfg.NUM_OF_VEINS_PER_NODE):

                # stroke_length = random.randint(cfg.MIN_STROKE_LENGTH, cfg.MIN_STROKE_LENGTH)
                # angle_change = random.uniform(cfg.MAX_ANGLE_CHANGE, cfg.MAX_ANGLE_CHANGE)
                
                end_x = random.randint(0, width)
                end_y = random.randint(0, height)

                # Difference cases depending on if we are simulating a cancer example or non cancer example
                if height >= cfg.MAX_ROWS // 2:
                    cancer_thick = cfg.LARGE_CANCER_STROKE
                    non_cancer_thick = cfg.LARGE_NO_CANCER_STROKE
                else:
                    cancer_thick = cfg.SMALL_CANCER_STROKE
                    non_cancer_thick = cfg.SMALL_NO_CANCER_STROKE
                
                if has_cancer:
                    # Generate a case of having cancer
                    cv2.line(veins_img, (start_x, start_y), (end_x, end_y), 1, thickness = cancer_thick)
                else:
                    # Generate a case of not having cancer
                    cv2.line(veins_img, (start_x, start_y), (end_x, end_y), 1, thickness = non_cancer_thick)

        self.veins_area = np.sum(veins_img)

        if self.visualize and height < 50001:             # Don't Visualise if the dimensions are more than 50,000
            plt.imshow(veins_img, cmap = 'gray')
            print("Displaying the Veins with dye with area", self.veins_area)
            plt.show()

        print("Fake veins generated.")

        return self._sparse_compress(veins_img)
    
    # Compressing and saving the parasite information using Run Length Encoding
    def _rle_compress(self, array, is_parasite = True): 
        print("compressing..")
        result = []
        array = array.flatten()
        curr_val = None
        count = 0

        for val in tqdm(array):
            if curr_val == None:

                curr_val = val
                count += 1
            else:
                if curr_val != val:
                    result.append([curr_val, count])
                    curr_val = val
                    count = 1
                else:
                    if count < 255:
                        count += 1
                    else:
                        result.append([curr_val, count])
                        curr_val = val
                        count = 1

        result.append([curr_val, count])

        self.rle_save(result)

        return result
    
    # Get back the original image from the compressed image
    def _rle_decompress(self, compressed_img):
        print("Decompressing...")
        decompressed_img = []
        for item in compressed_img:
            pixel_value, run_length = item
            decompressed_img.extend([pixel_value] * run_length)
        return np.array(decompressed_img, dtype=np.uint64).reshape(self.size)
    
    # Helper function to save the compressed parasite image as a .tif file
    def rle_save(self, compressed_img):
        
        print("Saving the parasite image in", cfg.DATA_DIR + '/parasite' + '/parasite_' + str(self.sess_num) +'.tif')
        cv2.imwrite(cfg.DATA_DIR + '/parasite' + '/parasite_' + str(self.sess_num) +'.tif', np.array(compressed_img))
        return
    
    # Function to compress 
    def _sparse_compress(self, array):

        print("Compressing the veins image...")
        # Stores the entire veins information as a dictionary following sparse matrix compression
        overall_result = {}
        # Stores only the veins inside the parasite body information as a dictionary following sparse matrix compression.
        # Make it faster to calculate overlap later. As we are passing through the veins image here itself.
        only_body_result = {}
        i = 0
        array = array.flatten()
        for val in tqdm(array):
            if val == 1:
                row = i // self.size[0]
                col = i % self.size[1]
                if self.parasite_img[row][col] == 1:
                    only_body_result[(row, col)] = True
                overall_result[(row, col)] = True
            i += 1
        return overall_result, only_body_result
    
    # To decompress the veins image
    def _sparse_decompress(self, veins_dict):

        raise NotImplementedError
    
    # Helper function to save the compressed veins image as a pickle file
    def sparse_save(self, veins_dict):

        # Saving to pickle file
        print("Saving the veins data in", cfg.DATA_DIR + '/veins' + '/veins_' + str(self.sess_num) +'.pkl')
        with open(cfg.DATA_DIR + '/veins' + '/veins_' + str(self.sess_num) +'.pkl', 'wb') as f:
            pickle.dump(veins_dict, f)
        return
    
    # Calculate if the parasite has cancer or not
    def calculate_overlap(self, parasite, veins_body_only):
        # we have already saved the information of veins that are strictly inside the body area. Hence we only need to divide.
        return len(veins_body_only) / self.parasite_area
            
        

# DRIVER CODE

if __name__ == '__main__':

    sess = 2
    simulate = Simulate(size = (1000, 1000), visualize = True, sess_num = sess)

    parasite = simulate.generate_fake_parasite()
    veins_all, veins_body = simulate.generate_fake_veins(has_cancer = False)
    print("Veins outside body are", len(veins_all) - len(veins_body))
    simulate.sparse_save(veins_dict = veins_all)

    # Finding cancer code here