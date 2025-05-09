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

cv2.imshow("Image with ROI", image_with_roi)
cv2.waitKey(0)
cv2.destroyWindow("Image with ROI")

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

for set in range(1,6):

    print(set)

    path_set_file="C:/Users/anama/OneDrive/Ambiente de Trabalho/UNI/Semestre2/ICSTS/Task3/ICSTS_EIT_Processment/Images/set_0"+str(set)

    items = os.listdir(path_set_file)
    files_num = len([item for item in items if os.path.isdir(os.path.join(path_set_file, item))])

    diff_expiration_trial=np.zeros(files_num)
    diff_inspiration_trial=np.zeros(files_num)

    for trial in range(1,files_num+1):

        print(str(trial))

        if trial > 9:
            images_file=sorted(glob("C:/Users/anama/OneDrive/Ambiente de Trabalho/UNI/Semestre2/ICSTS/Task3/ICSTS_EIT_Processment/Images/set_0"+str(set)+"/trial_"+str(trial)+'/*.png'))
        else:
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
        sum=0
        
        for i in expiration_frames:
            sum=sum+abs(processed_signal_left[i]-processed_signal_right[i])

        
        diff_expiration_trial[trial-1]=sum/files_num


        # Inspiration
        inspiration_frames=peak_detection(processed_signal_left,"inspiration")
        sum=0
        
        for i in inspiration_frames:
            sum=sum+abs(processed_signal_left[i]-processed_signal_right[i])

    
        diff_inspiration_trial[trial-1]=sum/len(inspiration_frames)

    diff_expiration_set[set-1]=np.sum(diff_expiration_trial)/files_num
    diff_inspiration_set[set-1]=np.sum(diff_inspiration_trial)/files_num

expiration_data=diff_expiration_set
inspiration_data=diff_inspiration_set


print("The following patients should be evaluated through other techniques of diagnosis:\n")
for patient in range(len(expiration_data)):
    if expiration_data[patient] > 0.5 or inspiration_data[patient] > 0.5:
        print("patient"+str(patient))

data = {
    'set 1': [expiration_data[0], inspiration_data[0]],
    'set 2': [expiration_data[1], inspiration_data[1]],
    'set 3': [expiration_data[2], inspiration_data[2]],
    'set 4': [expiration_data[3], inspiration_data[3]],
    'set 5': [expiration_data[4], inspiration_data[4]],
}

df = pd.DataFrame(data, index=['Expiration', 'Inspiration'])

print(df)



