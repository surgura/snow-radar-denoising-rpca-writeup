"""
Denoise data by dropping the first few singular values.

Saves results to 'results/svd_results.pickle'. See code for structure.
"""

import numpy as np
import pickle
import os
import scipy

data = np.load("data/data.npy")

results = {}
mu = 1.0 / np.sqrt(max(data.shape))
for dropx in [1, 4, 6, 10, 20]:
    print(f"SVD, dropping # singular values = {dropx}")
    u, s, v = scipy.linalg.svd(data, full_matrices=False)
    denoised = data - u[:, 0:dropx] @ np.diag(s[0:dropx]) @ v[0:dropx, :]
    results[f"denoised_dropx{dropx}"] = denoised

if not os.path.exists("results"):
    os.makedirs("results")
with open("results/svd_results.pickle", "wb") as f:
    pickle.dump(results, f)
