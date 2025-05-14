# Przetwarzanie A/C tworzą 3 etapy: próbkowanie, kwantyzacja i kodowanie.
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write, read


# funkcja nagrywa dźwięk z mikrofonu, dokonuje jego kwantyzacji i zapisuje do pliku .wav (A/C)
def record_audio(czas_nagrania=3, czestotliwosc_probkowania=44100, bity_kwantyzacji=16, wynikowy_plik="output.wav"):
    print(f"Recording at {czestotliwosc_probkowania} Hz, {bity_kwantyzacji}-bit...")
    print(f"Please, say something!")

    # NAGRYWANIE DŹWIĘKU
    # liczba próbek do nagrania -> czas_nagrania * czestotliwosc_probkowania
    # chennels = 1 -> dźwięk mono (monofoniczny) (identyczny dźwięk w obu uszach)
    # zakres [-1.0, 1.0] ?????
    audio = sd.rec(int(czas_nagrania * czestotliwosc_probkowania), samplerate=czestotliwosc_probkowania, channels=1,
                   dtype='float32')
    sd.wait()

    # KWANTYZACJA
    if bity_kwantyzacji == 8:
        audio_int = np.clip((audio * 127.5 + 127.5), 0, 255).astype(
            np.uint8)  # przesuwa i skaluje dźwięk z [-1.0, 1.0] do [0,255]
    elif bity_kwantyzacji == 16:
        audio_int = np.clip(audio * 32767, -32768, 32767).astype(
            np.int16)  # skaluje dźwięk z [-1.0, 1.0] do [-32768, 32767], skaluje się do 32767, żeby uniknąć przepełnienia int16
    else:
        raise ValueError("Unsupported bit depth")

    write(wynikowy_plik, czestotliwosc_probkowania, audio_int)  # zapisuje zakwantyzowany sygnał do pliku .wav
    print(f"Saved to {wynikowy_plik}")
    return audio, audio_int

# funkcja odtwarza plik dźwiękowy .wav za pomocą karty dźwiękowej (C/A)
def play_audio(filename):
    print(f"Playing {filename}...")
    czestotliwosc_probkowania, data = read(filename) # data - tablica z danymi audio
    sd.play(data, czestotliwosc_probkowania)
    sd.wait()

# funkcja oblicza współczynnika SNR (jak bardzo zniekształcony jest sygnał względem oryginału)
def calculate_snr(original, test):
    noise = original - test
    signal_power = np.sum(original ** 2) # moc sygnału jako suma kwadratów wartości sygnału
    noise_power = np.sum(noise ** 2) # moc szumu jako suma kwadraty błędów
    return 10 * np.log10(signal_power / noise_power) # wartość SNR w decybelach (im większe SNR, tym lepsza jakość dźwięku)


# MAIN -> testowanie różnych kombinacji częstotliwości próbkowania i bitów kwantyzacji
# czestotliwosci_probkowania = [8000, 22050, 44100, 96000]
# bity_kwantyzacji = [8, 16]
# czas_nagrania = 3  # sekundy
#
# wyniki = []
#
# for czestotliwosc in czestotliwosci_probkowania:
#     for bit in bity_kwantyzacji:
#         filename = f"rec_{czestotliwosc}Hz_{bit}bit.wav"
#         oryginal, po_kwantyzacji = record_audio(czas_nagrania, czestotliwosc, bit, filename)
#         play_audio(filename)
#         wyniki.append((czestotliwosc, bit, filename, oryginal, po_kwantyzacji))
#
# # SNR względem najlepszego nagrania
# najlepsze_nagranie = None
# for wynik in wyniki:
#     if wynik[0] == 96000 and wynik[1] == 16: # o czestotliwosci_probkowania 96000 i 16 bitach kwantyzacji
#         najlepsze_nagranie = wynik
#         break
# najlepszy_syngal = najlepsze_nagranie[3].flatten()
#
# print("\nSNR results:")
# for czestotliwosc, bit, filename, oryginal, po_kwantyzacji in wyniki:
#     try:
#         # dopasowanie długości sygnałów - UWAGA! PORÓWNUJE SIĘ Z DANYMI PRZED ZAPISANIEM DO PLIKU - NIE WIEM CZY NIE ZMIENIĆ
#         najlepszy_dopasowany_dlugoscia = najlepszy_syngal[:len(oryginal.flatten())]
#         snr = calculate_snr(najlepszy_dopasowany_dlugoscia, oryginal.flatten())
#         print(f"{czestotliwosc}Hz, {bit}-bit: SNR = {snr:.2f} dB")
#     except Exception as e:
#         print(f"Błąd dla {filename}: {e}")

czestotliwosc = 8000
bit = 8
czas_nagrania = 3
wyniki = []
filename = f"rec_{czestotliwosc}Hz_{bit}bit.wav"
oryginal, po_kwantyzacji = record_audio(czas_nagrania, czestotliwosc, bit, filename)
play_audio(filename)
wyniki.append((czestotliwosc, bit, filename, oryginal, po_kwantyzacji))
print(wyniki)