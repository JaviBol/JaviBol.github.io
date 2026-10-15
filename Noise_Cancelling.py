print("Project Idea - Noise Cancelling Headphones")
print("This project will use a microphone to pick up ambient noise and then generate an opposite sound wave to cancel out the noise. The user will be able to adjust the volume of the noise cancelling effect like a potentiometer.")

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import stft, istft

audio = None
sample_rate = None
noise_estimate = None
cleaned = None
strength = 1.0

def main_menu():
    while True:
        print("\nWelcome to the Active Noise Cancellation Simulator!")
        print("This program simulates the functionality of noise cancelling headphones.")
        print("Choose what action you'd like to run")
        print("1. Record new Audio File")
        print("2. Load existing Audio File")
        print("3. Apply noise cancelling effect to audio file")
        print("4. Adjust volume of noise cancelling effect")
        print("5. Show frequency spectrum of audio file")
        print("6. Exit")

        user_input = input("Please input your choice (1-6): ")

        if user_input == "1":
            print("Recording new audio file...")
            record_audio()
        elif user_input == "2":
            print("Loading existing audio file...")
            load_audio()
        elif user_input == "3":
            print("Applying noise cancelling effect to audio file...")
            apply_noise_cancel()
        elif user_input == "4":
            print("Adjusting volume of noise cancelling effect...")
            adjust_volume()
        elif user_input == "5":
            print("Showing frequency spectrum of audio file...")
            show_spectrum()
        elif user_input == "6":
            print("\nExiting Active Noise Cancellation Simulator. Thank you!")
            break
        else:
            print("Invalid input. Please choose a number between 1 and 6.")

def to_mono_float(data):
    """Convert wav data to mono floats between -1 and 1."""
    if data.dtype == np.int16:
        data = data / 32768.0
    elif data.dtype == np.int32:
        data = data / 2147483648.0
    elif data.dtype == np.uint8:
        data = (data - 128) / 128.0
    else:
        data = data.astype(np.float64)
    if data.ndim > 1:
        data = data.mean(axis=1)
    return data


def record_audio():
    global audio, sample_rate, cleaned, noise_estimate
    try:
        import sounddevice as sd
    except ImportError:
        print("Please run: pip install sounddevice")
        return
    seconds = input("How many seconds to record? (default 5): ").strip()
    seconds = int(seconds) if seconds.isdigit() else 5
    sample_rate = 44100
    print(f"Recording for {seconds} seconds... make some noise!")
    rec = sd.rec(int(seconds * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()
    audio = rec[:, 0]
    cleaned = noise_estimate = None
    filename = input("Save as (e.g. my_recording.wav): ").strip() or "recording.wav"
    wavfile.write(filename, sample_rate, (audio * 32767).astype(np.int16))
    print(f"Saved {filename}")


def load_audio():
    global audio, sample_rate, cleaned, noise_estimate
    path = input("Enter the .wav file name or path: ").strip().strip('"').strip("'")
    path = os.path.expanduser(path)
    if not os.path.exists(path):
        script_folder = os.path.dirname(os.path.abspath(__file__))
        alt = os.path.join(script_folder, path)
        if os.path.exists(alt):
            path = alt
    try:
        sample_rate, data = wavfile.read(path)
    except Exception as e:
        print("Could not load that file:", e)
        return
    audio = to_mono_float(data)
    cleaned = noise_estimate = None
    print(f"Loaded {path}: {len(audio) / sample_rate:.1f} seconds at {sample_rate} Hz")


def apply_strength():
    """Anti-noise = the opposite (negative) of the noise. Adding it cancels the noise."""
    global cleaned
    anti_noise = -noise_estimate
    cleaned = audio + strength * anti_noise


def apply_noise_cancel():
    global noise_estimate
    if audio is None:
        print("Load or record an audio file first (option 1 or 2).")
        return

    f, t, Z = stft(audio, sample_rate, nperseg=2048)
    magnitude = np.abs(Z)

    slice_loudness = magnitude.mean(axis=0)
    quiet = slice_loudness <= np.percentile(slice_loudness, 10)
    noise_profile = magnitude[:, quiet].mean(axis=1, keepdims=True)

    new_magnitude = np.maximum(magnitude - 2.0 * noise_profile, 0)
    Z_clean = new_magnitude * np.exp(1j * np.angle(Z))
    _, clean_signal = istft(Z_clean, sample_rate, nperseg=2048)

    clean_signal = np.resize(clean_signal, len(audio))

    noise_estimate = audio - clean_signal
    apply_strength()

    print("Noise cancelling applied!")
    freqs, removed = removed_spectrum()
    top = np.argsort(removed)[-5:][::-1]
    print("Frequencies with the most noise removed:")
    for i in top:
        print(f"  ~{freqs[i]:.0f} Hz")

    out = input("Save cleaned audio as (press Enter to skip): ").strip()
    if out:
        save_cleaned(out)


def save_cleaned(filename):
    peak = max(np.max(np.abs(cleaned)), 1e-9)
    data = cleaned / peak if peak > 1 else cleaned
    wavfile.write(filename, sample_rate, (data * 32767).astype(np.int16))
    print(f"Saved {filename}")


def adjust_volume():
    global strength
    if noise_estimate is None:
        print("Apply the noise cancelling effect first (option 3).")
        return
    value = input("Noise cancelling strength 0-100 (like turning the knob): ").strip()
    try:
        strength = min(max(float(value), 0), 100) / 100
    except ValueError:
        print("Please enter a number.")
        return
    apply_strength()
    print(f"Strength set to {strength * 100:.0f}%")
    out = input("Save cleaned audio as (press Enter to skip): ").strip()
    if out:
        save_cleaned(out)


def spectrum(signal):
    """Return frequencies and their strengths using the FFT."""
    spec = np.abs(np.fft.rfft(signal)) / len(signal)
    freqs = np.fft.rfftfreq(len(signal), 1 / sample_rate)
    return freqs, spec


def removed_spectrum():
    return spectrum(audio - cleaned)


def show_spectrum():
    if audio is None:
        print("Load or record an audio file first (option 1 or 2).")
        return
    freqs, orig = spectrum(audio)
    limit = min(8000, sample_rate / 2)

    if cleaned is None:
        plt.figure(figsize=(10, 4))
        plt.plot(freqs, orig)
        plt.xlim(0, limit)
        plt.title("Frequency Spectrum of Audio")
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Strength")
        plt.tight_layout()
        plt.show()
        return

    _, clean = spectrum(cleaned)
    _, removed = removed_spectrum()

    fig, axes = plt.subplots(3, 1, figsize=(10, 9), sharex=True)
    axes[0].plot(freqs, orig, color="tab:blue")
    axes[0].set_title("Original audio")
    axes[1].plot(freqs, clean, color="tab:green")
    axes[1].set_title("After noise cancelling")
    axes[2].plot(freqs, removed, color="tab:red")
    axes[2].set_title("Frequencies removed (the noise)")
    axes[2].set_xlabel("Frequency (Hz)")
    for ax in axes:
        ax.set_ylabel("Strength")
        ax.set_xlim(0, limit)
    plt.tight_layout()
    plt.show()


main_menu()