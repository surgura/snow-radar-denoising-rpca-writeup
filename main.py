import numpy as np
import matplotlib.pyplot as plt
import pickle
from pyrpca import rpca_pcp_ialm

data = np.load("data/data.npy")

low_rank, sparse = rpca_pcp_ialm(
    data,
    sparsity_factor=1.0 / np.sqrt(max(data.shape)),
)
with open("results/ialm.pickle", "wb") as f:
    pickle.dump({"l_ialm": low_rank, "s_ialm": sparse}, f)
# with open("results/ialm.pickle", "rb") as f:
#     results = pickle.load(f)
#     low_rank = results["l_ialm"]
#     sparse = results["s_ialm"]

fig, axes = plt.subplots(1, 2, figsize=(15, 5), constrained_layout=True)

# original data
axes[0].imshow(data, aspect="auto", cmap="gray")
axes[0].set_title("Original Data")

# low-rank component (noise)
axes[1].imshow(low_rank, aspect="auto", cmap="gray")
axes[1].set_title("Low-rank component")

# sparse component (hidden signal)
axes[1].imshow(sparse, aspect="auto", cmap="gray")
axes[1].set_title("Sparse component")

plt.show()
