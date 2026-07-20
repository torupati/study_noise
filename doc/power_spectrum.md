# Power Spectrum

## 1. Continuous-time definition

Let $x(t)$ be a continuous-time signal. Any "normal" signal can be reconstructed by

$$
 x(t) = \frac{1}{2\pi} \int_{\infty}^{\infty} \int_{\infty}^{\infty} x(t^\prime) e^{2\pi f (t-t^\prime)}df dt^\prime
$$

### Fourier Transform 

Its Fourier transform is

$$
X(f) = \lim_{T \to \infty}\int_{-T/2}^{T/2} x(t)e^{-j2\pi ft}dt
$$

Then the energy spectrum is proportional to

$$
|X(f)|^2
$$

For a power signal observed over a long interval $T$, the power spectral density can be written as

$$
S_x(f) = \lim_{T \to \infty} \frac{1}{T}|X_T(f)|^2
$$

where $X_T(f)$ is the Fourier transform of the time-limited signal.

In simple terms:

- $X(f)$ shows the frequency content.
- $|X(f)|^2$ shows the strength at each frequency.
- $S_x(f)$ is the continuous-time power spectrum density.

## 2. Discrete signal and FFT expression

Suppose we sample the signal and obtain

$$
x[n], \quad n = 0,1,2,\dots,N-1
$$

with sampling frequency $f_s$.

The $N$-point DFT is

$$
X[k] = \sum_{n=0}^{N-1} x[n] e^{-j2\pi kn/N}, \quad k = 0,1,2,\dots,N-1
$$

In practice, this is calculated with the FFT.

A simple discrete power spectrum estimate is

$$
P[k] = \frac{1}{N}|X[k]|^2
$$

If you want power spectral density in units per Hz, a common expression is

$$
PSD[k] = \frac{1}{Nf_s}|X[k]|^2
$$

The frequency corresponding to bin $k$ is

$$
f_k = \frac{k}{N}f_s
$$

Since observed signal is real value, spectrum is even. So we usually plot only half of it.


