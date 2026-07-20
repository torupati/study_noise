# One-Sided Power Spectral Density

If $S(f)$ is the two-sided Power Spectral Density and $G(f)$ is the one-sided Power Spectral Density, their relationship is as follows:

$$G(f)=2\cdot S(f)\quad \text{for\ }f>0$$

$$G(f)=0\quad \text{for\ }f<0$$

Feature | One-Sided PSD | Two-Sided PSD
 --- | --- | ---
Frequency Range | Positive frequencies only (0 to $f_{max}$) | Positive and negative frequencies ($-f_{max}$ to $f_{max}$)
Use Case / Preference | Standard in engineering, acoustics, and structural vibrations | Standard in physics and communications (e.g., RF, signal processing)
Amplitude | Values are multiplied by 2 to conserve total power | Values are typically half the magnitude of the one-sided PSD
Integration for Total Power | $\int_{0}^{\infty} G(f) \, df = \text{Total Power}$ | $\int_{-\infty}^{\infty} S(f) \, df = \text{Total Power}$

## References

- Matlab: [dspdata.psd](https://mathworks.com/help/signal/ref/dspdata.psd.html)
- DSP Related com: [Power Spectral Density](https://www.dsprelated.com/glossary/psd)
- 