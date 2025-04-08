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
mu = 1.0 / np.sqrt(max(data.shape))
for mu_factor in [0.5, 0.75, 1.0, 1.25, 1.5]:
    print(f"RPCA for mu factor = {mu_factor}")
    low_rank, sparse = rpca_pcp_ialm(
        data,
        sparsity_factor=mu_factor * mu,
    )
    results[f"l_muf{mu_factor}"] = low_rank
    results[f"s_muf{mu_factor}"] = sparse

if not os.path.exists("results"):
    os.makedirs("results")
with open("results/rpca_results.pickle", "wb") as f:
    pickle.dump(results, f)
