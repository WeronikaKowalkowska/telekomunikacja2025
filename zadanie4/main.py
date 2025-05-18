# Przetwarzanie A/C tworzą 3 etapy: próbkowanie, kwantyzacja i kodowanie.
import os
from pathlib import Path

import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write, read
from scipy.signal import resample


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

    folder = Path("files")
    folder.mkdir(exist_ok=True)
    file_path = folder / wynikowy_plik
    write(file_path, czestotliwosc_probkowania, audio_int)  # zapisuje skwantyzowany sygnał do pliku .wav
    print(f"Saved to {file_path}")
    return audio, audio_int


# funkcja odtwarza plik dźwiękowy .wav za pomocą karty dźwiękowej (C/A)
def play_audio(filename):
    print(f"Playing {filename}...")
    czestotliwosc_probkowania, data = read(filename)  # data - tablica z danymi audio
    sd.play(data, czestotliwosc_probkowania)
    sd.wait()


# funkcja oblicza współczynnika SNR (jak bardzo zniekształcony jest sygnał względem oryginału) - wyższe SNR oznacza lepszą jakość dźwięku
def calculate_snr(original, test):
    noise = original - test
    signal_power = np.sum(original ** 2)  # moc sygnału jako suma kwadratów wartości sygnału
    noise_power = np.sum(noise ** 2)  # moc szumu jako suma kwadraty błędów
    return 10 * np.log10(
        signal_power / noise_power)  # wartość SNR w decybelach (im większe SNR, tym lepsza jakość dźwięku)

def convert_signal(sygnal, nowa_czestotliwosc, nowe_bity):
    czestotliwosc_sygnalu = 96000

    # ZMIANA CZĘSTOTLIWOŚCI PRÓBKOWANIA
    # len(sygnal) - liczba próbek w oryginalnym sygnale
    # nowa_czestotliwosc / czestotliwosc_sygnalu - proporcja między nową i starą częstotliwością próbkowania
    nowa_liczba_probek = int(len(sygnal) * nowa_czestotliwosc / czestotliwosc_sygnalu)
    sygnal_nowy = resample(sygnal, nowa_liczba_probek)

    max = np.max(np.abs(sygnal_nowy)) # największa bezwzględna wartość sygnału
    if max == 0:    # czyli cisza -> zwracamy od razu (by nie dzielić przez 0)
        return sygnal_nowy

    # NORMALIZACJA amplitudy do przedziału [-1, 1]
    sygnal_nowy_normalizowany = sygnal_nowy / max

    # KWANTYZACJA
    if nowe_bity == 8:
        sygnal_nowy_kwant = np.clip((sygnal_nowy_normalizowany * 127.5 + 127.5), 0, 255).astype(
            np.uint8)  # przesuwa i skaluje dźwięk z [-1.0, 1.0] do [0,255]
        sygnal_koncowy = (sygnal_nowy_kwant.astype(np.float32) - 127.5) / 127.5
    elif nowe_bity == 16:
        sygnal_nowy_kwant = np.clip(sygnal_nowy_normalizowany * 32767, -32768, 32767).astype(
            np.int16)  # skaluje dźwięk z [-1.0, 1.0] do [-32768, 32767], skaluje się do 32767, żeby uniknąć przepełnienia int16
        sygnal_koncowy = sygnal_nowy_kwant.astype(np.float32) / 32767
    else:
        raise ValueError("Unsupported bit depth")

    return sygnal_koncowy.astype(np.float32)

while True:
    wybor = input(
        "Choose a converter: a) A/C b) C/A\nOr if you want to test different combinations of sampling rates and bit depth press c): ").lower()
    if wybor == "a" or wybor == "b" or wybor == "c":
        break
    else:
        raise ValueError("Unsupported converter, choose 'a', 'b' or 'c'.")

if wybor == "a":
    print("You can now record sound from a microphone. The program will quantize it and save it to a file.")
    czas_nagrania = None
    czestotliwosc_probkowania = None
    bity_kwantyzacji = None
    while True:
        czas_nagrania = int(input("Choose a recording duration (in seconds): 3 or 5  "))
        if czas_nagrania == 3 or czas_nagrania == 5:
            break
        else:
            raise ValueError("Unsupported recording duration, choose '3' or '5'.")
    while True:
        czestotliwosc_probkowania = int(input("Choose a sampling rate (Hz): 8000, 22050, 44100, or 96000  "))
        if czestotliwosc_probkowania in [8000, 22050, 44100, 96000]:
            break
        else:
            raise ValueError("Unsupported sampling rate, choose '8000', '22050', '44100', or '96000'.")
    while True:
        bity_kwantyzacji = int(input("Choose the bit depth: 8 or 16 bits  "))
        if bity_kwantyzacji == 8 or bity_kwantyzacji == 16:
            break
        else:
            raise ValueError("Unsupported bit depth, choose '8' or '16'.")
    filename = f"rec_{czestotliwosc_probkowania}Hz_{bity_kwantyzacji}bit.wav"
    oryginal, po_kwantyzacji = record_audio(czas_nagrania, czestotliwosc_probkowania, bity_kwantyzacji, filename)
elif wybor == "b":
    print("You can choose the .wav file. The program will play the audio file using the sound card.")
    wybrany_plik = None
    while True:
        folder = Path("files")
        lista_plikow = list(folder.glob("*.wav"))
        if not lista_plikow:
            print("No .wav files found.")
        else:
            print("Select a file:")
            for i, file in enumerate(lista_plikow):
                print(f"{i + 1}. {file.name}")

            index = int(input(
                "Enter the number of the file to select: ")) - 1  # numeracja listy od zera, dlatego odejmujemy zera
            if not index < 0 or index >= len(lista_plikow):
                wybrany_plik = lista_plikow[index]
                print(f"You selected: {wybrany_plik}")
                break
            else:
                print("No .wav file with this number. Please, try again.")
    play_audio(wybrany_plik)
elif wybor == "c":
    czestotliwosci_probkowania = [8000, 22050, 44100, 96000]
    bity_kwantyzacji = [8, 16]
    czas_nagrania = 3

    # nagranie raz, w najwyższej jakości
    oryginal, _ = record_audio(czas_nagrania, 96000, 16, "test.wav")

    play_audio("files/test.wav")

    wyniki = []
    najlepsze_nagranie = None

    for czestotliwosc in czestotliwosci_probkowania:
        for bit in bity_kwantyzacji:
            po_kwantyzacji = convert_signal(oryginal, czestotliwosc, bit)
            if czestotliwosc == 96000 and bit == 16:
                najlepsze_nagranie = po_kwantyzacji.flatten()
            wyniki.append((czestotliwosc, bit, "test.wav", po_kwantyzacji))

    # SNR względem najlepszego nagrania
    print("\nSNR results:")
    for czestotliwosc, bit, filename, po_kwantyzacji in wyniki:
        try:
            # resamplowanie najlepszego sygnału do porównywanej długości
            najlepszy_dopasowany = resample(najlepsze_nagranie, len(po_kwantyzacji.flatten()))
            snr = calculate_snr(najlepszy_dopasowany, po_kwantyzacji.flatten())
            print(f"{czestotliwosc}Hz, {bit}-bit: SNR = {snr:.2f} dB")
        except Exception as e:
            print(f"Błąd dla {filename}: {e}")
