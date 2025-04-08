"""
Denoise data by dropping the first few principal components.

Saves results to 'results/pca_results.pickle'. See code for structure.
"""

import numpy as np
import pickle
import os
from sklearn.decomposition import PCA

data = np.load("data/data.npy")

results = {}
mu = 1.0 / np.sqrt(max(data.shape))
for dropx in [1, 4, 6, 10, 15]:
    print(f"PCA, dropping # components = {dropx}")
    pca = PCA()
    pca_fit = pca.fit_transform(data)
    pca_fit[:, :dropx] = 0
    denoised = pca.inverse_transform(pca_fit)

    results[f"denoised_dropx{dropx}"] = denoised

if not os.path.exists("results"):
    os.makedirs("results")
with open("results/pca_results.pickle", "wb") as f:
    pickle.dump(results, f)
