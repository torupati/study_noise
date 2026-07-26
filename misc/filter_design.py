import numpy as np
import matplotlib.pyplot as plt

def design_fir_lpf(sr: float, f_cutoff: float, num_taps: int = 255) -> np.ndarray:
	"""Design a Hamming-windowed sinc FIR low-pass filter."""
	if not (0.0 < f_cutoff < sr / 2.0):
		raise ValueError("f_cutoff must satisfy 0 < f_cutoff < sr/2")
	if num_taps % 2 == 0:
		raise ValueError("num_taps must be odd for a symmetric linear-phase FIR")

	n = np.arange(num_taps)
	center = (num_taps - 1) / 2.0
	fc = f_cutoff / sr
	h_ideal = 2.0 * fc * np.sinc(2.0 * fc * (n - center))
	window = np.hamming(num_taps)
	h = h_ideal * window
	#h /= np.sum(h)
	return h

def filter_freq_response(b: np.ndarray, a: np.ndarray, freq: np.ndarray, sr: float) -> np.ndarray:
	"""Evaluate digital filter frequency response for arbitrary-length b and a."""
	b = np.asarray(b, dtype=float)
	a = np.asarray(a, dtype=float)
	if b.ndim != 1 or a.ndim != 1:
		raise ValueError("b and a must be 1-D arrays")
	if len(a) == 0 or len(b) == 0:
		raise ValueError("b and a must be non-empty")

	w = 2.0 * np.pi * freq / sr
	z = np.exp(-1j * w)
	num = np.zeros_like(z, dtype=complex)
	den = np.zeros_like(z, dtype=complex)

	for k, bk in enumerate(b):
		num += bk * (z ** k)
	for k, ak in enumerate(a):
		den += ak * (z ** k)

	return num / den


def moving_average_coefficients(num_samples: int) -> np.ndarray:
	"""Return FIR coefficients for an N-point moving average filter."""
	if num_samples <= 0:
		raise ValueError("num_samples must be a positive integer")
	return np.ones(num_samples, dtype=float) / num_samples


def robust_unwrapped_phase_deg(
	h: np.ndarray,
	freq: np.ndarray,
	sr: float,
	num_samples: int,
	mag_threshold: float = 1e-6,
) -> np.ndarray:
	"""Unwrap phase on valid regions and align each region to linear-phase expectation."""
	mag = np.abs(h)
	phase = np.full(h.shape, np.nan, dtype=float)
	valid = mag > mag_threshold
	expected = -np.pi * (num_samples - 1) * freq / sr

	if not np.any(valid):
		return phase

	indices = np.where(valid)[0]
	splits = np.where(np.diff(indices) > 1)[0] + 1
	segments = np.split(indices, splits)

	for seg in segments:
		local_phase = np.unwrap(np.angle(h[seg]))
		# Phase of MA filter is ambiguous by k*pi around sign changes of the real factor.
		# Align each segment to the expected linear-phase branch.
		k = int(np.round(np.mean((expected[seg] - local_phase) / np.pi)))
		phase[seg] = local_phase + k * np.pi

	return phase * 180.0 / np.pi


def theoretical_linear_phase_deg(freq: np.ndarray, sr: float, num_samples: int) -> np.ndarray:
	"""Return theoretical linear phase of an N-point moving average FIR in degrees."""
	return -180.0 * (num_samples - 1) * freq / sr


def plot_moving_average_response(sr: float = 1000.0, num_samples: int = 20, output_path: str = "doc/pictures/ma20_response.png") -> None:
	"""Plot frequency response of a moving average filter and save as PNG."""
	b = moving_average_coefficients(num_samples)
	a = np.array([1.0], dtype=float)
	freq = np.linspace(0.0, sr / 2.0, 4096)
	h = filter_freq_response(b, a, freq, sr)

	mag = np.abs(h)
	mag_db = 20.0 * np.log10(np.maximum(mag, 1e-12))
	phase_deg = robust_unwrapped_phase_deg(h, freq, sr, num_samples, mag_threshold=1e-4)
	theory_phase_deg = theoretical_linear_phase_deg(freq, sr, num_samples)

	fig, axes = plt.subplots(3, 1, figsize=(10, 9), sharex=True)
	axes[0].plot(freq, mag, color="tab:blue", linewidth=2)
	axes[0].set_ylabel("Magnitude")
	axes[0].set_title(f"{num_samples}-sample moving average frequency response (fs={sr:.0f} Hz)")
	axes[0].grid(True, alpha=0.3)

	axes[1].plot(freq, mag_db, color="tab:red", linewidth=2)
	axes[1].set_ylabel("Magnitude [dB]")
	axes[1].set_ylim(-80, 5)
	axes[1].grid(True, alpha=0.3)

	axes[2].plot(freq, phase_deg, color="tab:green", linewidth=2, label="Measured phase")
	axes[2].plot(freq, theory_phase_deg, color="black", linestyle="--", linewidth=1.5, label="Theoretical linear phase")
	axes[2].set_xlabel("Frequency [Hz]")
	axes[2].set_ylabel("Phase [deg]")
	axes[2].grid(True, alpha=0.3)
	axes[2].legend(loc="upper right")
	axes[2].set_xlim([freq[0], freq[-1]])

	fig.tight_layout()
	fig.savefig(output_path, dpi=150)
	plt.close(fig)


if __name__ == "__main__":
	plot_moving_average_response(sr=1000.0, num_samples=20)


