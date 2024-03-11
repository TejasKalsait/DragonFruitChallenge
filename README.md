# Submission to the Image Compression Coding Challenge
### by Tejas Kalsait

This repository contains code for efficient representation of microscope and dye sensor images, creation of simulated images, parasite cancer detection, optimization for speed, and exploration of compression techniques.

# Method

## Simulation

- Parasites are envisioned as blobs that are quite random but contiguous and occupy >25% of the image.
- Veins are envisioned as thin and random strings.

To generate these images, I created a `Simulation()` class that handles the creation and compression of these images. I ensured the veins covered the part outside the parasite's body too, to create a more realistic scenario.

## Compression

As the images are going to be `100,000 x 100,000` in dimension, it is important to compress them as most of the information in the image is irrelevant. For example, in the parasite image, we do not care about the part which is outside the body. Hence, it can be discarded.
I brainstormed several methods to compress the images and found that the best methods would be -
- **Run-Length-Encoding for the parasite image**
- **Sparse Matrix Compression for the veins image**

#### Run-Length-Encoding
- Run-length encoding (RLE) in binary images is a simple compression technique used to represent consecutive sequences of the same pixel value (0 or 1) as a single value followed by the count of how many times it occurs.
- RLE is particularly useful in binary images because it can significantly reduce the storage space required to represent the image. Since binary images often consist of large areas of uniform color (`which is exactly the parasite image type`), RLE can efficiently compress these regions by storing the value and length of each run instead of each pixel. I have also made sure that all the values after compression fit within `8-bits` to save even more space.
- The generated images are then saved as `.tif` file, which is lossless and thus helps us benchamark our compression capacity better.

#### Sparse-Matrix-Compression
- Sparse matrix compression is a technique used to efficiently store and manipulate matrices that contain a significant number of zero values. Instead of storing all elements of the matrix, sparse matrix compression only stores the non-zero elements along with their corresponding row and column indices.
- In our case, the veins image mostly contains zero values. It was given in the instruction that less than 0.1 percent of parasites will have cancer. That means, `999 out of every 1000 images will have less than 10% of the area with value 1 (veins).` Therefore, for storing the veins, Sparse matrix compression performs extremely well. (We'll get to actual storage numbers soon).
- The generated images are then saved as `a pickle file`, which is lossless and thus helps us directly import the pickle file into a Python dictionary.

> [!NOTE]
> I have made sure I use compression techniques that are lossless and I have coded functions `_rle_decompress()` and `_sparse_decompress()` that build the original image back from the compressed format.

# Results

## Memory
- The baseline (naive method) of storing the one image would take 100,000 * 100,000 * 1 byte per pixel = 10GB of memory
- We can improve the storage by using the `BitMatrixMethod` which uses only 1 bit to store pixel information. Therefore, 100,000 * 100,000 * 1 bit per pixel = 1.25GB
- After running the RLE compression on the parasite image, the storage occupied is only **`520 kb`**. That is `0.0051%` of the baseline
- After running the sparse matrix compression on the veins image, the storage occupied is only `22.2 mb`. That is `0.22%` of the baseline. And these are only going to be of the cancer detected parasite which is less than 0.1% of total.

> [!NOTE]
> The Simulator class has been implemented in a way that it performs all calculations on the compressed formats with clever algorithms. Hence it saves RAM and runs faster.


## My Output
__________________________________________________________________________________________
Fake parasite generated.
compressing...
Saving the parasite image in data/parasite/parasite_1.tif
__________________________________________________________________________________________
Fake veins generated.
Compressing the veins image...
__________________________________________________________________________________________
-------- PART 1 RESULTS ---------
No cancer detected in the parasite 1
Overlap found to be 0.021071981545192936
__________________________________________________________________________________________
Fake parasite generated.
compressing...
Saving the parasite image in data/parasite/parasite_2.tif
__________________________________________________________________________________________
Fake veins generated.
Compressing the veins image...
__________________________________________________________________________________________
-------- PART 2 RESULTS ---------
No cancer detected in the parasite 2
Overlap found to be 0.05229889275546684

# Contact Information
- LinkedIn - https://www.linkedin.com/in/tkalsait/
- Portfolio - https://tejaskalsait.github.io/

> Summary - I’m leading the development of a Digital Twin and Co-Simulator for SUNY Buffalo’s autonomous vehicle leveraging advanced machine learning techniques and frameworks such as PyTorch, AWSIM, and Autoware. We have engineered scalable and high-performance data pipelines for processing gigabytes of LIDAR sensor data, to generate high-fidelity virtual environments replicating real-world scenes for use in Unreal and Unity engines. Improved object detection accuracy by 15% compared to leading open-sourced software using a custom YOLOv8 model, leading to an enhanced and robust autonomous navigation system.

# Thank You
