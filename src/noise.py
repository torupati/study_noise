import numpy as np


def simulate_white_noise(n_samples: int, fs: float, sigma: float = 1.0, random_state=None) -> np.ndarray:
    """Generate Gaussian white noise samples of a sensor with specified length and sampling frequency.

    Args:
        n_samples: Number of samples to generate.
        fs: Sampling frequency in Hz
        sigma: noise density in Unit/rt-Hz (NOT standard deviation of the noise).
        random_state: Seed or numpy Generator-compatible state.

    Returns:
        Array of shape (n_samples,) with zero-mean Gaussian white noise.
    """
    rng = np.random.default_rng(random_state)
    return rng.normal(loc=0.0, scale=sigma, size=n_samples) * np.sqrt(fs)


def compute_power_spectrum(x: np.ndarray, fs: float, spectrum_type: str = "double-sided") -> tuple[np.ndarray, np.ndarray]:
    """Compute power spectral density (PSD) via the periodogram.

    Uses the FFT-based periodogram with density scaling so PSD has units of V**2/Hz.

    Args:
        x: Real-valued time series samples.
        fs: Sampling frequency in Hz.
        spectrum_type: "double-sided" or "one-sided" PSD. Default is "double-sided".

    Returns:
        freqs: Array of non-negative frequencies (Hz).
        psd: PSD values corresponding to freqs.
    """
    if spectrum_type not in ("double-sided", "one-sided"):
        raise ValueError("spectrum_type must be 'double-sided' or 'one-sided'")
    x = np.asarray(x)
    N = x.size
    # FFT of the signal
    X = np.fft.rfft(x)
    # Two-sided PSD estimate (density) = (1/(fs*N)) * |X|^2
    psd = (1.0 / (fs * N)) * (np.abs(X) ** 2)
    if spectrum_type == "one-sided":
        if N % 2 == 0:
            # even N: last bin is Nyquist and should not be doubled
            if psd.size > 2:
                psd[1:-1] *= 2
        else:
            if psd.size > 1:
                psd[1:] *= 2
    else:
        # For double-sided, include negative frequencies by mirroring the positive side
        psd = np.concatenate((psd, psd[-2:0:-1]))
    freqs = np.fft.rfftfreq(N, d=1.0 / fs)
    return freqs, psd
