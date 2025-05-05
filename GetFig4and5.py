"""
Bibliotecas

"""

import numpy as np
import os
from glob import glob
import matplotlib.pyplot as plt
from pathlib import Path
import pandas as pd

"""
functions

"""

from functions import *

"""
Definição da RoI

"""

# Abrir e Ler um Frame
path_frame="C:/Users/anama/OneDrive/Ambiente de Trabalho/UNI/Semestre2/ICSTS/Task3/ICSTS_EIT_Processment/Images/set_01/trial_01/frame_004.png"
image_test = cv2.imread(path_frame)


## Selecionar manualmente RoI Pulmão Esquerdo
#r_left=cv2.selectROI("select the area left", image)
#cv2.destroyWindow("select the area left")

## Selecionar manualmente RoI Pulmão Direito
#r_right=cv2.selectROI("select the area right", image)
#cv2.destroyWindow("select the area right")

# Coordenadas obtidas com zona anterior comentada
r_left=220, 169, 194, 339 
r_right=498, 169, 194, 339

# Representação da zona RoI do pulmão esquero
r=r_left
image_with_roi = image_test.copy()
cv2.rectangle(image_with_roi, (r[0], r[1]), (r[0] + r[2], r[1] + r[3]), (0, 0, 255), 2)  # Criar rectangulo vermelho

# Abrir e Ler todos os Frames
diff_expiration_set=np.zeros(5)
diff_inspiration_set=np.zeros(5)


sample_image_left = apply_RoI(path_frame, r_left)
sample_image_right = apply_RoI(path_frame, r_right)

# Example shape from first image
sample_array_left = np.array(sample_image_left)
sample_array_right = np.array(sample_image_right)

height_l, width_l, channels_l = sample_array_left.shape
height_r, width_r, channels_r = sample_array_right.shape



set=2
trial=1

path_set_file="C:/Users/anama/OneDrive/Ambiente de Trabalho/UNI/Semestre2/ICSTS/Task3/ICSTS_EIT_Processment/Images/set_0"+str(set)

items = os.listdir(path_set_file)
files_num = len([item for item in items if os.path.isdir(os.path.join(path_set_file, item))])

diff_expiration_trial=np.zeros(files_num)
diff_inspiration_trial=np.zeros(files_num)



images_file=sorted(glob("C:/Users/anama/OneDrive/Ambiente de Trabalho/UNI/Semestre2/ICSTS/Task3/ICSTS_EIT_Processment/Images/set_0"+str(set)+"/trial_0"+str(trial)+'/*.png'))

image_array_left = np.zeros((len(images_file), height_l, width_l, channels_l), dtype=np.uint8)

image_array_right = np.zeros((len(images_file), height_r, width_r, channels_r), dtype=np.uint8)

for image_num in range(len(images_file)):

    image_left = apply_RoI(images_file[image_num], r_left)
    image_right = apply_RoI(images_file[image_num], r_right)

    image_array_left[image_num]=image_left
    image_array_right[image_num]=image_right


impedance_signal_left=impedance_calc(image_array_left)
impedance_signal_right=impedance_calc(image_array_right)

processed_signal_left=processing(impedance_signal_left)
processed_signal_right=processing(impedance_signal_right)

# Expiration
expiration_frames=peak_detection(processed_signal_left,"expiration")

# Inspiration
inspiration_frames=peak_detection(processed_signal_left,"inspiration")

# Load the image corresponding to the first expiration frame
image_expiration = cv2.imread(images_file[expiration_frames[0]])

# Define output path and filename
output_path = "C:/Users/anama/OneDrive/Ambiente de Trabalho/UNI/Semestre2/ICSTS/Task3/ICSTS_EIT_Processment/output"
os.makedirs(output_path, exist_ok=True)  # Create folder if it doesn't exist
output_filename = os.path.join(output_path, f"expiration_frame_patient_{set}.png")

# Save the image
cv2.imwrite(output_filename, image_expiration)
print(f"Expiration image saved to: {output_filename}")

