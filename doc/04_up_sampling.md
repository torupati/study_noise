# Up Sampling

Here is my understanding how to calculate higher sampling rate signal from low sampling rate.

## 

Let's think 1024 sample in one second.
N=1024. Fs = 1024 Hz.
Period = 256 step, or 0.25 sec.
Frequency is 1024/256 = 4 Hz

$f(t) = \sin(2\pi F_0 t)$

$f[n] = \sin(2\pi F_0 n/F_s) = \sin(2\pi \cdot 0.25 * n / N)$