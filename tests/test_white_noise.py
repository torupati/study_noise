import numpy as np
from src.noise import simulate_white_noise, compute_power_spectrum


def test_white_noise_psd_mean_close_to_expected():
    fs = 1000.0
    time_len = 3.0
    N = int(fs * time_len)
    sigma = 0.345
    # generate reproducible noise
    x = simulate_white_noise(N, fs, sigma=sigma, random_state=42)
    freqs, psd = compute_power_spectrum(x, fs)
    # exclude DC (index 0) and Nyquist (last index if present) from mean
    if N % 2 == 0:
        psd_bins = psd[1:-1]
    else:
        psd_bins = psd[1:]
    mean_psd = float(np.mean(psd_bins))
    mean_psd = float(np.mean(psd))
    # For one-sided PSD estimated as implemented, expected level ~ 2*sigma^2/fs
    #expected = 2.0 * (sigma ** 2) / fs
    expected = sigma ** 2
    # allow 5% relative tolerance for randomness
    rel_err = abs(mean_psd / expected - 1.0)
    assert rel_err < 0.05, f"mean_psd={mean_psd:.6e}, expected={expected:.6e}, rel_err={rel_err:.3%}"
