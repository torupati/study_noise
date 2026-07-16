# Simulation of noise density.  Random
#
import matplotlib.pyplot as plt
import numpy as np
rng = np.random.default_rng()

# white noise V/sqrt(Hz) = V sqrt(T)
# converted to level by multiplying sqrt(Hz) or devided by sqrt(dt)
# rondom walk --> white noise if differentiated. V sqrt(T)^3
sig_noise = 0.13 # Volt/sqrt(Hz)  
time_length = 0.5 # s
sr = 44100 # sammpling rate [Hz] = [1/s]

sample_num = int(sr * time_length)
print(f'{sample_num=}')

white_noise = sig_noise * np.sqrt(sr) * rng.standard_normal(sample_num+100)
x_td = np.cumsum(white_noise[100:]) / (sr)
#x_td = x_td - np.mean(x_td)
x_timdindex = [ i / sr for i in range(sample_num)]
x_mean = np.mean(x_td)


M = 8192*2
x_fd = np.fft.fft(x_td, n=M)
x_freqindex = [ i / len(x_fd) * sr for i in range(len(x_fd))]

pwr_fd = (x_fd * x_fd.conj()).real 

print("")
print(f"sig2 = {sig_noise**2=}")
print(f"{np.mean(np.abs(x_fd)**2 / sr / sample_num)=}")
print("")
#input()

fig, axs = plt.subplots(2, 1)

ax = axs[0]
ax.plot(x_timdindex, x_td, ".", markersize=1)
ax.set_xlim([0, time_length])
ax.set_xlabel('time [s]')
ax.grid(True)
ax.legend(loc='lower right')


ax = axs[1]
ax.plot(x_freqindex, np.abs(x_fd)**2 / sr / sample_num, ".", markersize=1, label='sim')
ax.plot(x_freqindex[1:], [sig_noise**2/((2*np.pi*f)**2) for f in x_freqindex[1:]], ".", markersize=1, label=r"$\frac{\sigma^2}{(2\pi f)^2}$")
ax.set_yscale('log')
#ax.set_xscale('log')
ax.set_xlim([0, sr/2])
ax.set_xlabel('frequency [Hz]')
ax.grid(True)
ax.legend(loc='upper right')
fig.tight_layout()
fig.savefig('out.png')

