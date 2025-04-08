import matplotlib.pyplot as plt
import pickle
import numpy as np

data = np.load("data/data.npy")
with open("results/rpca_results.pickle", "rb") as f:
    results = pickle.load(f)

fig, axes = plt.subplots(3, 2, figsize=(15, 10), constrained_layout=True, sharey=True)

# original data
axes[0][0].imshow(data, aspect="auto", cmap="gray")
axes[0][0].set_title("Original Data")
axes[0][0].set_xlabel("Sample index")
axes[0][0].set_ylabel("Time index")

# sparse components (hidden signal)
for ax, mu_factor in zip(axes.flatten()[1:], [0.5, 0.75, 1.0, 1.25, 1.5], strict=True):
    ax.imshow(results[f"s_muf{mu_factor}"], aspect="auto", cmap="gray")
    ax.set_title(f"Sparse component ({mu_factor} * mu)")
    ax.set_xlabel("Sample index")

plt.savefig("rpca_result.png")
plt.show()
