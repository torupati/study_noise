# White Noise

White noise is a random signal whose power spectral density is flat. The inverse Fourier transform of the power spectral density is the autocorrelation, which is nonzero only when the time points coincide.

$$
R(t_1,t_2) = \sigma^2 \delta(t_1 - t_2)
$$

or it depends only on time lag in the stationary state,

$$
R(\tau) = \sigma^2 \delta(\tau)
$$

Here $\sigma$ is noise density.

## Simulation

If we simulate this as a discrete signal, for example with sampling rate $F_s$ [Hz] ($F_s$ samples per second), how can we generate the signal? Let's assume $x(t)$ is a signal from some sensor. The unit of $x(t)$ might be voltage, or a physical unit like degree per second (dps) in a gyroscope, g in an accelerometer, and so on.

We can sample an independently distributed random variable $w_i$ from a Gaussian distribution in computation.

$$
x_i = \sigma\sqrt{F_s}\,w_i = \frac{\sigma}{\sqrt{T_s}} w_i
$$

$$
w_i \sim N(0,1)
$$


### Power Spectrum and Noise Density

Here is a example calculation of sensor white noise. This simulation takes sampling rate, noise density and time length as input. You can verify that the result is independet from the sampling rate, using python script. Spectrum density should be always $\sigma^2$ with any sampling rate, in the unit of valtage square per Hertz.

![image info](./pictures/whitenoise_time_and_input_psd.png)



### Filtering

Usually sensor data is sampled periodically after passed filtering for anti-aliasing and noise reduction. Here we simulate the case that our simulated white noise is filterd with IIR and FIR low-pass filter. You can see that power density at high frequency is reduced from original noise with both filters.

![image info](./pictures/whitenoise_psd_fir_iir.png)

