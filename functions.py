import scipy
from PIL import Image
import numpy as np
from scipy.ndimage import gaussian_filter1d
import cv2

def apply_RoI(image,r):
    
    image = Image.open(image)
    image_np = np.array(image)
    image= image_np[int(r[1]):int(r[1]+r[3]),int(r[0]):int(r[0]+r[2])] 
    
    return image

def impedance_calc(image_array):

    impedance_means = []

    for image in image_array:
    
        # Convert to grayscale if needed, or to HSV to isolate intensity
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        intensity = hsv[:, :, 2]  # Value channel often correlates with impedance

        # Compute variance of pixel values (impedance variance estimate)
        mean_intensity = np.mean(intensity)
        impedance_means.append(mean_intensity)
    
    return impedance_means

def processing(signal):
    
    # Mudança da Frequência
    signal = np.array(signal)
    fps = 33
    num_seconds = len(signal) // fps
    signal_freq = signal[:num_seconds * fps].reshape(num_seconds, fps).mean(axis=1)

    # Normalização
    normalized_signal = (signal_freq - np.mean(signal_freq)) / np.std(signal_freq)

    # Filtrar
    smoothed_signal = gaussian_filter1d(normalized_signal, sigma=2)

    processed_signal=smoothed_signal

    return processed_signal

def peak_detection(signal,type):

    if type=="expiration":
        peak_time=scipy.signal.find_peaks(signal)[0]
    elif type == "inspiration":
        peak_time=scipy.signal.find_peaks(-signal)[0]
    else:
        print("Error: Inserted Type does not exist")

    return peak_time

def diff_calc(signal,type):

    if type=="expiration":
        peak_time=scipy.signal.find_peaks(signal)[0]
    elif type == "inspiration":
        peak_time=scipy.signal.find_peaks(-signal)[0]
    else:
        print("Error: Inserted Type does not exist")
    
    frames=peak_time*33

    return frames
