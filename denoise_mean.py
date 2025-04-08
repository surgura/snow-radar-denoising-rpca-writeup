"""
Denoise data using mean subtraction.

Saves results to 'results/mean_results.pickle'. See code for structure.
"""

import numpy as np
import pickle
import os
from matplotlib import pyplot as plt

data = np.load("data/data.npy")

mean = np.mean(data, axis=1)
mean_tiled = np.tile(mean.reshape((data.shape[0], 1)), (1, data.shape[1]))
denoised = data - mean_tiled

if not os.path.exists("results"):
    os.makedirs("results")
with open("results/mean_results.pickle", "wb") as f:
    pickle.dump({"mean": mean, "mean_tiled": mean_tiled, "denoised": denoised}, f)
