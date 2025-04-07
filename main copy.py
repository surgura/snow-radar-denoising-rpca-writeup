import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import FastICA

arr = np.load("data/rxraw.npy")

fig, ax = plt.subplots(3, 1, figsize=(10, 5))
ax[0].imshow(arr, cmap='gray', aspect='auto')

# Transpose for ICA: shape (11448 time, 511 sensors)
arr_T = arr.T

# Run FastICA
ica = FastICA(n_components=2, max_iter=1000, random_state=0)
sources = ica.fit_transform(arr_T)       # shape: (11448, 2)
mixing = ica.mixing_                     # shape: (511, 2)

# Reconstruct full signal (just to compare)
reconstructed_full = ica.inverse_transform(sources).T  # shape: (511, 11448)

# Compute per-source additive contributions
# Each source[:, i] is (11448,), mixing[:, i] is (511,)
# Outer product gives (11448, 511), transpose to (511, 11448)
source_contributions = np.array([
    np.outer(sources[:, i], mixing[:, i]).T for i in range(2)
])  # shape: (2, 511, 11448)

# Confirm sum equals full reconstruction
reconstruction_sum = np.sum(source_contributions, axis=0)
assert np.allclose(reconstruction_sum, reconstructed_full, atol=1e-6)

ax[1].imshow(source_contributions[0], cmap='gray', aspect='auto')
ax[2].imshow(source_contributions[1], cmap='gray', aspect='auto')

# ica = FastICA(n_components=2, max_iter=1000, random_state=0)
# sources = ica.fit_transform(arr.T)     # shape: (11448, 2)
# components = ica.components_           # shape: (2, 511)
# reconstructed = sources.T[:, :, np.newaxis] * components[:, np.newaxis, :]

# ax[1].imshow(reconstructed[0], cmap='gray', aspect='auto')
# ax[2].imshow(reconstructed[1], cmap='gray', aspect='auto')

# plt.show()