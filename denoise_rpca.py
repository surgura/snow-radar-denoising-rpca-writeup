"""
Denoise data using RPCA.

Saves results to 'results/rpca_results.pickle'. See code for structure.
"""

import numpy as np
import pickle
from pyrpca import rpca_pcp_ialm
import os

data = np.load("data/data.npy")

results = {}
lmbda = 1.0 / np.sqrt(max(data.shape))
for lmbda_factor in [0.5, 1.0, 1.25, 1.5, 2.0]:
    print(f"RPCA for lmbda factor = {lmbda_factor}")
    low_rank, sparse = rpca_pcp_ialm(
        data,
        sparsity_factor=lmbda_factor * lmbda,
    )
    results[f"l_lmbdaf{lmbda_factor}"] = low_rank
    results[f"s_lmbdaf{lmbda_factor}"] = sparse

if not os.path.exists("results"):
    os.makedirs("results")
with open("results/rpca_results.pickle", "wb") as f:
    pickle.dump(results, f)
