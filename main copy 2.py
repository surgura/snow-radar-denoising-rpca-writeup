import numpy as np
import matplotlib.pyplot as plt
import rpca.ealm
import rpca.ialm
import pickle

arr = np.load("data/rxraw.npy")
# arr = arr[:, :200]


# L_ealm, S_ealm = rpca.ealm.fit(arr)
L, S = rpca.ialm.fit(arr, lambda_=1.0 / np.sqrt(max(arr.shape)), max_iter=5000)
with open("results/ialm.pickle", "wb") as f:
    pickle.dump({"l_ialm": L, "s_ialm": S}, f)
# with open("results/ialm.pickle", "rb") as f:
#     data = pickle.load(f)
#     L = data["l_ialm"]
#     S = data["s_ialm"]
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Original Data
axes[0].imshow(arr, aspect='auto', cmap='gray')
axes[0].set_title('Original Data')

# Low-Rank Component
axes[1].imshow(L, aspect='auto', cmap='gray')
axes[1].set_title('Low-Rank Component')

# Sparse Component
axes[2].imshow(S, aspect='auto', cmap='gray')
axes[2].set_title('Sparse Component')

plt.tight_layout()
plt.show()