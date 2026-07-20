# LPF

### Ideal Low-Pass Filter

We derive FIR filter coefficients from the frequency response of an ideal low-pass filter, which passes frequencies below a cutoff and rejects frequencies above it.

The inverse Fourier transform of a rectangular frequency response is a sinc function.

$$
H(f)=
\begin{cases}
1, & |f|\le f_c\\
0, & |f|>f_c
\end{cases}
$$
The inverse Fourier transform is
$$
h(t)=2f_c\,\mathrm{sinc}(2f_ct)
$$
.

### FIR Design

The ideal low-pass filter is represented by a sinc function in the time domain. In FIR design, this ideal response is truncated to a finite length.

- Truncate it around the center by limiting the number of taps
- Apply a window function such as a Hamming window

This gives a straightforward way to realize low-pass behavior. Main characteristics are:

- **linear phase** (The coefficients can be made symmetric)
- **stable** (since it's FIR filter)

