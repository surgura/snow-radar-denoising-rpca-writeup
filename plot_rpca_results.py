import matplotlib.pyplot as plt
import pickle
import numpy as np

data = np.load("data/data.npy")
with open("results/rpca_results.pickle", "rb") as f:
    results = pickle.load(f)
    low_rank = results["l_ialm"]
    sparse = results["s_ialm"]

fig, axes = plt.subplots(1, 2, figsize=(15, 5), constrained_layout=True, sharey=True)

# original data
axes[0].imshow(data, aspect="auto", cmap="gray")
axes[0].set_title("Original Data")
axes[0].set_xlabel("Sample index")
axes[0].set_ylabel("Time index")

# sparse component (hidden signal)
axes[1].imshow(sparse, aspect="auto", cmap="gray")
axes[1].set_title("Sparse component")
axes[1].set_xlabel("Sample index")

plt.savefig("rpca_result.png")
plt.show()
