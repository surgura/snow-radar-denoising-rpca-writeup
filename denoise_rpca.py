"""
Denoise data using RPCA.

Saves results to 'results/rpca_results.pickle'. See code for structure.
"""

import numpy as np
import pickle
from pyrpca import rpca_pcp_ialm
import os

data = np.load("data/data.npy")

low_rank, sparse = rpca_pcp_ialm(
    data,
    sparsity_factor=1.0 / np.sqrt(max(data.shape)),
)

if not os.path.exists("results"):
    os.makedirs("results")
with open("results/rpca_results.pickle", "wb") as f:
    pickle.dump({"l_ialm": low_rank, "s_ialm": sparse}, f)
