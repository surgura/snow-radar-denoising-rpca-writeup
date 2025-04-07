import numpy as np
import matplotlib.pyplot as plt
import pickle
from rpca import RobustPCA

arr = np.load("data/rxraw.npy")
# arr = arr[:, :200]

rpca = RobustPCA(verbose=True)#(arr, lambda_=1.0 / np.sqrt(max(arr.shape)), max_iter=5000)
L, S = rpca.fit(arr)
with open("results/ialm.pickle", "wb") as f:
    pickle.dump({"l_ialm": L, "s_ialm": S}, f)
# with open("results/ialm.pickle", "rb") as f:
#     data = pickle.load(f)
#     L = data["l_ialm"]
#     S = data["s_ialm"]
fig, axes = plt.subplots(1, 2, figsize=(15, 5))

# Original Data
axes[0].imshow(arr, aspect='auto', cmap='gray')
axes[0].set_title('Original Data')

# # Low-Rank Component
# axes[1].imshow(L, aspect='auto', cmap='gray')
# axes[1].set_title('Low-Rank Component')

# Sparse Component
axes[1].imshow(S, aspect='auto', cmap='gray')
axes[1].set_title('Sparse Component')

plt.tight_layout()
plt.show()