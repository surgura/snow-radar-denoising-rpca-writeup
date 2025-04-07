import numpy as np
from numpy.linalg import norm
from scipy.sparse.linalg import svds

def shrink(X, tau):
    """Soft thresholding"""
    return np.sign(X) * np.maximum(np.abs(X) - tau, 0.0)

def svt(X, tau, rank=None):
    """Singular value thresholding"""
    m, n = X.shape
    full_svd = rank is None or rank >= min(m, n)
    if full_svd:
        U, s, Vt = np.linalg.svd(X, full_matrices=False)
    else:
        # partial SVD for speed
        U, s, Vt = svds(X, k=rank)
        # svds returns sorted smallest to largest
        idx = np.argsort(-s)
        U, s, Vt = U[:, idx], s[idx], Vt[idx, :]
    s_thresh = shrink(s, tau)
    nonzero = s_thresh > 0
    return U[:, nonzero] @ np.diag(s_thresh[nonzero]) @ Vt[nonzero, :]

def rpca_ialm(D, lambda_=None, tol=1e-7, max_iter=1000, mu=None, mu_max=1e7, rho=1.5, svd_rank=50, verbose=True):
    """
    Robust PCA via IALM. Returns L (low-rank) and S (sparse) such that D = L + S.
    """
    m, n = D.shape
    norm_D = norm(D, ord='fro')

    if lambda_ is None:
        lambda_ = 1 / np.sqrt(max(m, n))
    if mu is None:
        mu = 1.25 / norm_D  # suggested by Lin et al.

    L = np.zeros((m, n))
    S = np.zeros((m, n))
    Y = np.zeros((m, n))

    for it in range(max_iter):
        # Step 1: Update L via Singular Value Thresholding
        L = svt(D - S + (1/mu) * Y, 1/mu, rank=svd_rank)

        # Step 2: Update S via shrinkage
        S = shrink(D - L + (1/mu) * Y, lambda_ / mu)

        # Step 3: Dual variable update
        Z = D - L - S
        Y += mu * Z

        # Step 4: Check convergence
        err = norm(Z, ord='fro') / norm_D
        if verbose and it % 10 == 0:
            print(f"Iter {it:4d}: error={err:.2e}, rank(L)={np.linalg.matrix_rank(L)}, nnz(S)={np.sum(S != 0)}")

        if err < tol:
            break

        mu = min(mu * rho, mu_max)

    return L, S