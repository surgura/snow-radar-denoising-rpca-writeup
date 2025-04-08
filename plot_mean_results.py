import matplotlib.pyplot as plt
import pickle
import numpy as np

data = np.load("data/data.npy")
with open("results/mean_results.pickle", "rb") as f:
    results = pickle.load(f)
    mean = results["mean"]
    mean_tiled = results["mean_tiled"]
    denoised = results["denoised"]

fig, axes = plt.subplots(2, 2, figsize=(15, 8), constrained_layout=True)

vmin = data.min()
vmax = data.max()

# original data
axes[0][0].imshow(data, aspect="auto", cmap="gray", vmin=vmin, vmax=vmax)
axes[0][0].set_title("Original Data")
axes[0][0].set_xlabel("Sample index")
axes[0][0].set_ylabel("Time index")

# mean
axes[0][1].plot(mean)
axes[0][1].set_title("Mean")
axes[0][1].set_xlabel("Time index")
axes[0][1].set_ylabel("Signal strength")

# mean tiled
axes[1][0].imshow(mean_tiled, aspect="auto", cmap="gray", vmin=vmin, vmax=vmax)
axes[1][0].set_title("Mean copied for all samples")
axes[1][0].set_xlabel("Sample index")
axes[1][0].set_ylabel("Time index")

# denoised
axes[1][1].imshow(denoised, aspect="auto", cmap="gray")
axes[1][1].set_title("Denoised (mean subtracted from original)")
axes[1][1].set_xlabel("Sample index")
axes[1][1].set_ylabel("Time index")

plt.savefig("mean_result.png")
plt.show()
