import numpy as np


def simulate_white_noise(n_samples: int, fs: float, sigma: float = 1.0, random_state=None) -> np.ndarray:
    """Generate Gaussian white noise samples.

    Args:
        n_samples: Number of samples to generate.
        fs: Sampling frequency in Hz (not used for generation but kept for API symmetry).
        sigma: Standard deviation of the noise.
        random_state: Seed or numpy Generator-compatible state.

    Returns:
        Array of shape (n_samples,) with zero-mean Gaussian white noise.
    """
    rng = np.random.default_rng(random_state)
    return rng.normal(loc=0.0, scale=sigma, size=n_samples) * np.sqrt(fs)


def compute_power_spectrum(x: np.ndarray, fs: float):
    """Compute one-sided power spectral density (PSD) via the periodogram.

    Uses the FFT-based periodogram with density scaling so PSD has units of V**2/Hz.

    Args:
        x: Real-valued time series samples.
        fs: Sampling frequency in Hz.

    Returns:
        freqs: Array of non-negative frequencies (Hz).
        psd: One-sided PSD values corresponding to freqs.
    """
    x = np.asarray(x)
    N = x.size
    # FFT of the signal
    X = np.fft.rfft(x)
    # Two-sided PSD estimate (density) = (1/(fs*N)) * |X|^2
    psd = (1.0 / (fs * N)) * (np.abs(X) ** 2)
    # Convert to one-sided PSD: multiply non-DC and non-Nyquist bins by 2
    #if N % 2 == 0:
    #    # even N: last bin is Nyquist and should not be doubled
    #    if psd.size > 2:
    #        psd[1:-1] *= 2
    #else:
    #    if psd.size > 1:
    #        psd[1:] *= 2
    freqs = np.fft.rfftfreq(N, d=1.0 / fs)
    return freqs, psd
