# RPCA
 
import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import svd
 
def shrinkage_operator(X, tau):
    return np.sign(X) * np.maximum(np.abs(X) - tau, 0)
 
def singular_value_thresholding(X, tau):
    U, S, Vt = svd(X, full_matrices=False)
    S_thresh = np.maximum(S - tau, 0)
    return U @ np.diag(S_thresh) @ Vt
 
def rpca(D, lambda_param=None, tol=1e-7, max_iter=1000):

    m, n = D.shape
    if lambda_param is None:
        lambda_param = 1 / np.sqrt(max(m, n))
 
    # Initialize variables
    L = np.zeros_like(D)
    S = np.zeros_like(D)
    Y = D / np.max(np.abs(D))  # Normalize dual variable
    mu = 1.25 / np.linalg.norm(D, ord=2)  # Step size
    mu_bar = mu * 1e7
    rho = 1.5
    norm_D = np.linalg.norm(D, 'fro')
 
    for i in range(max_iter):
        print(i)
        # Update Low-rank component
        L = singular_value_thresholding(D - S + (1 / mu) * Y, 1 / mu)
       
        # Update Sparse component
        S = shrinkage_operator(D - L + (1 / mu) * Y, lambda_param / mu)
       
        # Update dual variable
        Y += mu * (D - L - S)
       
        # Update mu
        mu = min(mu * rho, mu_bar)
       
        # Check convergence
        err = np.linalg.norm(D - L - S, 'fro') / norm_D
        print(err)
        if err < tol:
            break
 
    return L, S
 

# Apply RPCA and visualize results
arr = np.load("data/rxraw.npy")
image = arr
 
# L, S = rpca(image)
L, S = rpca(image, lambda_param= 1 / np.sqrt(max(image.shape)), max_iter=1000, tol=1e-7)
 
# Plot original, low-rank, and sparse components
fig, axes = plt.subplots(1, 3, figsize=(12, 4))
axes[0].imshow(image, cmap='gray')
axes[0].set_title("Original Image")
axes[0].axis('off')
 
axes[1].imshow(L, cmap='gray')
axes[1].set_title("Low-Rank (Background)")
axes[1].axis('off')
 
axes[2].imshow(S, cmap='gray')
axes[2].set_title("Sparse (Foreground/Anomalies)")
axes[2].axis('off')
 
plt.tight_layout()
 

# plt.Figure()
# plt.imshow(S, cmap='gray')
plt.show()