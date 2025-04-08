"""
Creates an example waveform image from the results from RPCA denoising.

First run 'denoise_rpca.py'.
"""

import matplotlib.pyplot as plt
import pickle
import numpy as np

data = np.load("data/data.npy")
with open("results/rpca_results.pickle", "rb") as f:
    results = pickle.load(f)
    low_rank = results["l_ialm"]
    sparse = results["s_ialm"]

plt.figure(constrained_layout=True)
plt.plot(sparse[:, 0])
plt.xlabel("Time index")
plt.ylabel("Signal strength")
plt.savefig("example_waveform.png")

plt.figure(constrained_layout=True)
plt.imshow(sparse, aspect="auto", cmap="gray")
plt.xlabel("Sample index")
plt.ylabel("Time index")
plt.savefig("example_waveform_stack.png")

plt.figure(constrained_layout=True)
plt.imshow(data, aspect="auto", cmap="gray")
plt.xlabel("Sample index")
plt.ylabel("Time index")
plt.savefig("example_noisy_waveform_stack.png")
