import matplotlib.pyplot as plt
import pickle
import numpy as np

data = np.load("data/data.npy")
with open("results/pca_results.pickle", "rb") as f:
    results = pickle.load(f)

fig, axes = plt.subplots(3, 2, figsize=(15, 10), constrained_layout=True, sharey=True)

# original data
axes[0][0].imshow(data, aspect="auto", cmap="gray")
axes[0][0].set_title("Original Data")
axes[0][0].set_xlabel("Sample index")
axes[0][0].set_ylabel("Time index")

# sparse components (hidden signal)
for ax, dropx in zip(axes.flatten()[1:], [1, 4, 6, 10, 15], strict=True):
    ax.imshow(results[f"denoised_dropx{dropx}"], aspect="auto", cmap="gray")
    ax.set_title(f"Sparse component (dropped {dropx} largest components)")
    ax.set_xlabel("Sample index")

plt.savefig("pca_result.png")
plt.show()
