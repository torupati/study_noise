# Simulation of noise density. White Noise.
# Calculation is maybe correct.
#
import matplotlib.pyplot as plt
import numpy as np
rng = np.random.default_rng()

sig_noise = 0.13 # Volt / sqrt(Hz) noise density
time_length = 0.2 # s
sr = 44100 # sammpling rate [Hz] = [1/s]

sample_num = int(sr * time_length)
print(f'{sample_num=}')

x_td = sig_noise * np.sqrt(sr) * rng.standard_normal(sample_num) # Volt, nosie level 
x_timdindex = [ i / sr for i in range(sample_num)]
x_mean = np.mean(x_td)
x_std = np.sqrt(np.var(x_td, axis=0))
x_std2 = np.sqrt(np.sum(x_td * x_td) / sample_num)
print(f'{x_mean=}')
print(f'{x_std=} {sig_noise * np.sqrt(sr)=}')
print(f'{x_std2=}')

M = 8192
x_fd = np.fft.fft(x_td, n=M)
x_freqindex = [ i / len(x_fd) * sr for i in range(len(x_fd))]
print(f"{np.sum(x_td * x_td)=}") # EU*EU
print(f"{np.sum(x_fd * x_fd.conj()) / len(x_fd)=}") # EU*EU = EU/rt(Hz) **2 * Hz
print(f"{np.sum(np.abs(x_fd)**2) / len(x_fd)=}") # EU*EU = EU/rt(Hz) **2 * Hz
print("--")

pwr_fd = (x_fd * x_fd.conj()).real 

print("")
print(f"sig2 = {sig_noise**2=}")
print(f"{np.mean(np.abs(x_fd)**2 / sr / sample_num)=}")
print("")
input()

fig, axs = plt.subplots(2, 1)

ax = axs[0]
ax.plot(x_timdindex, x_td, ".", markersize=1)
ax.axhline(y=sig_noise *np.sqrt(sr), label=r"$\sigma/\sqrt{T}$", color='red', linewidth=1)
ax.axhline(y=-sig_noise *np.sqrt(sr), label=r"$-\sigma/\sqrt{T}$", color='red', linewidth=1)
ax.set_xlim([0, time_length])
ax.set_xlabel('time [s]')
ax.grid(True)
ax.legend(loc='lower right')


ax = axs[1]
ax.plot(x_freqindex, np.abs(x_fd)**2 / sr / sample_num, ".", markersize=1)
#ax.axhline(y=np.mean(pwr_fd), label=r"$E[Y]$", color='green')
ax.axhline(y=sig_noise**2 , label=r"$\sigma^2$", color='red')
ax.set_yscale('log')
#ax.set_xscale('log')
ax.set_xlim([0, sr/2])
ax.set_xlabel('frequency [Hz]')
ax.grid(True)
ax.legend(loc='lower right')
fig.tight_layout()
fig.savefig('whitenoise.png')

