import numpy as np
from scipy.fft import fft

def classify_sound(audio):
    fft_vals = np.abs(fft(audio))
    energy = np.sum(fft_vals)
    mean_freq = np.mean(fft_vals)
    if energy < 10000:
        label = "silence"
    elif np.mean(fft_vals[:500]) > np.mean(fft_vals[500:]):
        label = "speech"
    else:
        label = "music/noise"
    return {"label": label, "energy": float(energy), "mean_freq": float(mean_freq)}
