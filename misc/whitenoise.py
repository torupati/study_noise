import matplotlib.pyplot as plt
import numpy as np


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


def psd_realin(x: np.ndarray, sr: float) -> tuple[np.ndarray, np.ndarray]:
	"""Return PSD estimate from FFT."""
	n = len(x)
	x_fft = np.fft.rfft(x)
	psd = (np.abs(x_fft) ** 2) / (n * sr)
	#if n > 2:
#		psd[1:-1] *= 2.0
	freq = np.fft.rfftfreq(n, d=1.0 / sr)
	return freq, psd


def design_iir_butterworth_lpf(sr: float, f_cutoff: float) -> tuple[np.ndarray, np.ndarray]:
	"""Design a 2nd-order digital Butterworth LPF (biquad)."""
	if not (0.0 < f_cutoff < sr / 2.0):
		raise ValueError("f_cutoff must satisfy 0 < f_cutoff < sr/2")

	k = np.tan(np.pi * f_cutoff / sr)
	norm = 1.0 / (1.0 + np.sqrt(2.0) * k + k * k)
	b0 = k * k * norm
	b1 = 2.0 * b0
	b2 = b0
	a1 = 2.0 * (k * k - 1.0) * norm
	a2 = (1.0 - np.sqrt(2.0) * k + k * k) * norm

	b = np.array([b0, b1, b2], dtype=float)
	a = np.array([1.0, a1, a2], dtype=float)
	return b, a


def apply_iir_filter(x: np.ndarray, b: np.ndarray, a: np.ndarray) -> np.ndarray:
	"""Apply an IIR filter using direct-form difference equation."""
	y = np.zeros_like(x, dtype=float)
	for n in range(len(x)):
		x0 = x[n]
		x1 = x[n - 1] if n >= 1 else 0.0
		x2 = x[n - 2] if n >= 2 else 0.0
		y1 = y[n - 1] if n >= 1 else 0.0
		y2 = y[n - 2] if n >= 2 else 0.0
		y[n] = b[0] * x0 + b[1] * x1 + b[2] * x2 - a[1] * y1 - a[2] * y2
	return y


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


# White-noise density [Volt/sqrt(Hz)]
sig_noise = 0.03
time_length = 30.0  # [s]
sr = 400  # [Hz]
f_cutoff = sr * 0.25
num_taps = 11

sample_num = int(sr * time_length)
t_sample = 1.0 / sr
t_axis = np.arange(sample_num) / sr

# Generate white noise and apply FIR/IIR filters.
x_td = sig_noise / np.sqrt(t_sample) * np.random.normal(0.0, 1.0, sample_num)
# FIR low-pass filter design and application.
h_fir = design_fir_lpf(sr=sr, f_cutoff=f_cutoff, num_taps=num_taps)
x_td_lpf = np.convolve(x_td, h_fir, mode="same")
# IIR low-pass filter design and application.
b_iir, a_iir = design_iir_butterworth_lpf(sr=sr, f_cutoff=f_cutoff)
x_td_iir = apply_iir_filter(x_td, b_iir, a_iir)

freq, psd_in = psd_realin(x_td, sr)
_, psd_fir = psd_realin(x_td_lpf, sr)
_, psd_iir = psd_realin(x_td_iir, sr)

# One-sided theoretical white-noise PSD based on noise density.
psd_in_theory = np.full_like(freq, sig_noise**2)
#psd_in_theory[0] = sig_noise**2

fir_h = filter_freq_response(h_fir, np.array([1.0]), freq, sr)
iir_h = filter_freq_response(b_iir, a_iir, freq, sr)
psd_fir_theory = psd_in_theory * (np.abs(fir_h) ** 2)
psd_iir_theory = psd_in_theory * np.abs(iir_h) ** 2

print(f"sample_num={sample_num}")
print(f"f_cutoff={f_cutoff:.2f} Hz, num_taps={num_taps}")
print(f"input std={np.std(x_td):.6f}")
print(f"FIR filtered std={np.std(x_td_lpf):.6f}")
print(f"IIR filtered std={np.std(x_td_iir):.6f}")

# Figure 1: time-domain signals + input PSD only.
fig1, axs1 = plt.subplots(2, 1, figsize=(10, 7))
fig1.suptitle(
	f"White Noise Time Domain and Frequency Domain\n"
	f"noise density={sig_noise} V/rt-Hz, sr={sr} Hz, T={time_length:.1f} s"
)

ax = axs1[0]
ax.set_title("Time-domain signals")
ax.plot(t_axis, x_td, ".", markersize=1, alpha=0.5, label="simulated noise")
#ax.plot(t_axis, x_td_lpf, "-", linewidth=1.0, alpha=0.8, label="FIR filtered noise")
#ax.plot(t_axis, x_td_iir, "-", linewidth=1.0, alpha=0.8, label="IIR filtered noise")
ax.set_xlim([0, time_length])
ax.set_xlabel("time [s]")
ax.set_ylabel("amplitude [V]")
ax.grid(True)
ax.legend(loc="upper right")

ax = axs1[1]
ax.set_title("Input Power Spectral Density (PSD)")
ax.plot(freq, psd_in, ".", markersize=1, alpha=0.6, label="input PSD")
ax.plot(freq, psd_in_theory, "-", linewidth=1.8, label="input PSD (theory)")
#ax.axvline(f_cutoff, color="red", linewidth=1.2, linestyle="--", label="F_cutoff")
ax.set_yscale("log")
ax.set_xlim([0, sr / 2.0])
ax.set_xlabel("frequency [Hz]")
ax.set_ylabel("PSD [V^2/Hz]")
ax.grid(True)
ax.legend(loc="upper right")

fig1.tight_layout()
fig1.savefig("whitenoise_time_and_input_psd.png", dpi=140)

# Figure 2: PSD comparison + overlaid filter responses.
fig2, ax_psd = plt.subplots(1, 1, figsize=(10, 5.5))
fig2.suptitle(
	f"PSD Comparison with FIR/IIR Responses (F_cutoff={f_cutoff:.1f} Hz, FIR taps={num_taps})\n"
	f"noise density={sig_noise} V/rt-Hz, sr={sr} Hz"
)

ax_psd.set_title("Power Spectral Density (PSD)")
ax_psd.plot(freq, psd_in, ".", markersize=1, alpha=0.45, label="input PSD")
ax_psd.plot(freq, psd_fir, ".", markersize=1, alpha=0.7, label="FIR filtered PSD")
ax_psd.plot(freq, psd_iir, ".", markersize=1, alpha=0.7, label="IIR filtered PSD")
ax_psd.plot(freq, psd_in_theory, "-", linewidth=1.3, label="input PSD (theory)")
ax_psd.plot(freq, psd_fir_theory, "-", linewidth=1.6, label="FIR PSD (theory)")
ax_psd.plot(freq, psd_iir_theory, "-", linewidth=1.6, label="IIR PSD (theory)")
ax_psd.axvline(f_cutoff, color="red", linewidth=1.2, linestyle="--", label="F_cutoff")
ax_psd.set_yscale("log")
ax_psd.set_xlim([0, sr / 2.0])
ax_psd.set_ylim([1e-10, 1e-1])
ax_psd.set_xlabel("frequency [Hz]")
ax_psd.set_ylabel("PSD [V^2/Hz]")
ax_psd.grid(True)

#ax_resp = ax_psd.twinx()
#fir_resp_db = 20.0 * np.log10(np.maximum(np.abs(fir_h), 1e-12))
#iir_resp_db = 20.0 * np.log10(np.maximum(np.abs(iir_h), 1e-12))
#ax_resp.plot(freq, fir_resp_db, "--", linewidth=1.3, alpha=0.9, label="FIR response [dB]")
#ax_resp.plot(freq, iir_resp_db, "--", linewidth=1.3, alpha=0.9, label="IIR response [dB]")
#ax_resp.set_ylabel("Filter response [dB]")

handles_psd, labels_psd = ax_psd.get_legend_handles_labels()
#handles_resp, labels_resp = ax_resp.get_legend_handles_labels()
#ax_psd.legend(
#	handles_psd + handles_resp,
#	labels_psd + labels_resp,
#	loc="upper left",
#	bbox_to_anchor=(1.02, 1.0),
#	borderaxespad=0.0,
#)
ax_psd.legend(
		handles_psd,
		labels_psd,
		loc="upper left",
		bbox_to_anchor=(1.02, 1.0),
		borderaxespad=0.0,
)

fig2.tight_layout(rect=[0.0, 0.0, 0.82, 1.0])
fig2.savefig("whitenoise_psd_fir_iir_response.png", dpi=140)

# Figure 3: FIR coefficients (impulse response).
fig3, ax_imp = plt.subplots(1, 1, figsize=(8, 4.5))
fig3.suptitle(
	f"FIR Impulse Response (num_taps={num_taps}, F_cutoff={f_cutoff:.1f} Hz, sr={sr} Hz)"
)

tap_idx = np.arange(len(h_fir))
ax_imp.set_title("FIR filter coefficients")
ax_imp.stem(tap_idx, h_fir, linefmt="C0-", markerfmt="C0o", basefmt="k-")
ax_imp.set_xlabel("tap index")
ax_imp.set_ylabel("coefficient")
ax_imp.grid(True)

fig3.tight_layout()
fig3.savefig("fir_impulse_response.png", dpi=140)
