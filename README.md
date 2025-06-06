# Write-up on snow radar denoising using Robust Principal Component Analysis
This is a write-up of a small signal processing project I completed. It explains the thought process I followed and introduces Robust Principal Component Analysis (RPCA), which aims to separate a data matrix into a linearly regular part and a sparse, mostly empty part. I hope to encourage other scientists and engineers to explore the recently growing field of sparse and low-rank optimization, as it may prove surprisingly effective for seemingly difficult tasks.

## Update - Heads up
This is blind denoising strategy primarily targeted at removing coherent noise (flight height independent noise). While it is a great way to learn about RPCA, you can generally do better my modeling the system properly. Currently, I am working to apply techniquies related to this repository to remove the coherent noise and subsequently remove the effects of an imperfect radar system by approximating the radar impulse response from a set of waveforms, supporting deconvolution. I will update this repository whenever that is done.

## The problem
The Norwegian Research Center (NORCE) researches methods of remotely measuring snow depth. In one of their projects, a drone equipped with a radar was used to fly over terrestrial snow, sending and receiving radar signals[[1]](#jenssen2023). A typical 'waveform' looks like this:

![Example waveform](example_waveform.png)

You can concatenate multiple waveforms to create an image where pixel intensity represents signal strength:

![Example waveform stack](example_waveform_stack.png)

However, in reality, the signal is extremely noisy. You can barely see the underlying structure.

![Example noisy waveform stack](example_noisy_waveform_stack.png)

This happens because the antennas used are not very directional. As a result, the receiving antenna picks up not only the intended reflections from the snow target but also unwanted signals, including those reflected by the drone itself. The data must be preprocessed before the underlying signal can be analyzed.

## Method 1: Naive mean subtraction
Most of the noise is caused by the measurement instrument itself. This is fortunate, as it means the noise is independent of the measurement location and therefore highly correlated between waveforms.

I started with the naive approach of assuming the noise is identical across waveforms and estimating it by averaging them. I then subtracted this average from each waveform. See the script `denoise_mean.py`. This results in the following:

![Naive mean subtraction result](mean_result.png)

The latent signal is clearly more visible, but some noise remains.

## Method 2: Singular value high pass filter
One of the postprocessing methods used at NORCE is to apply singular value decomposition (SVD) and discard the first few singular values. This makes sense, as SVD identifies linear relationships in the data, and the noise is clearly correlated between samples. The script `denoise_svd.py` implements this approach, producing the following result:

![SVD result](svd_result.png)

This looks better than simply subtracting the mean. The result is also tunable via the number of components removed. However, some noise still remains, and discarding too many components starts degrading the signal instead of improving it.

## Method 3: Robust principal component analysis
In recent years, a technique called Robust Principal Component Analysis (RPCA) has gained popularity[[2]](#candes2011). This algorithm separates a matrix into two parts: one sparse (many zeros) and one low-rank (rows are highly correlated; i.e., there is a lot of linear structure). Our noise is clearly low-rank, as our earlier methods (mean subtraction and SVD) already perform reasonably well. The latent signal also appears sparse, as suggested by our preliminary results. This makes our problem an ideal candidate for RPCA.

RPCA refers to a matrix decomposition problem where the goal is to separate a dataset into a low-rank component and a sparse component. Multiple algorithms exist to solve or approximate this decomposition. I implemented a simple Python package for RPCA[[3]](#stuurmanpyrpca) that solves the PCP convex relaxation using the IALM algorithm. It's not essential to understand the algorithmic details here, but the repository provides technical references.

RPCA has only one important parameter: lambda. This controls the trade-off between sparsity and low-rank structure. I experimented with different values in the script `denoise_rpca.py`, with the results shown below.

![RPCA result](rpca_result.png)

I believe RPCA extracts the underlying signal very effectively. It is easily tunable through a single parameter, which has clear and interpretable effects. Lower values permit more noise, while higher values enforce more sparsity, leading to a visible and intuitive trade-off. The only downside of RPCA is that it is an optimization problem and can take time to solve. However, in this case, the matrix is quite small and runs quickly. There are also ways to speed things up, such as processing the data in smaller chunks (even in parallel) or using alternative optimization techniques or improved versions of IALM.

## Conclusion
I hope this write-up offers some insight into the more niche RPCA algorithm and shows what’s possible beyond common noise reduction techniques. RPCA works exceptionally well for this use case and can be adapted to many other problems. Although slower than simpler methods, it remains practical and there are various ways to improve its performance. The next time you encounter noisy data, I encourage you to try RPCA and other sparse and low-rank optimization techniques.

## References
1. <a name="jenssen2023"></a> [R.-O. R. Jenssen. Snow depth from UAV GPR. Norwegian Meteorological Institute (2023).](https://doi.org/10.21343/ZAW8-2G80) Raw, unprocessed data from the original study was used for this project. A small subset of this raw data is included in the repository for demonstration purposes. The reference points to the full study, which includes processed data products, although the raw dataset itself is not publicly available.
2. <a name="candes2011"></a> [Emmanuel J. Candès, Xiaodong Li, Yi Ma, John Wright. Robust principal component analysis? Association for Computing Machinery 2011.](https://doi.org/10.1145/1970392.1970395) (preprint on [arXiv](https://doi.org/10.48550/arXiv.0912.3599))
3. <a name="stuurmanpyrpca"></a> [A. C. Stuurman (me). github.com/surgura/PyRPCA v1.0.0, Robust PCA for Python.](https://github.com/surgura/PyRPCA)
