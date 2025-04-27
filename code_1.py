"""
Bibliotecas

"""

import cv2
import numpy as np
import os
import glob
import matplotlib.pyplot as plt
from PIL import Image
import scipy
from scipy.ndimage import gaussian_filter1d
from pathlib import Path


"""
Definição da RoI

"""

# Abrir e Ler um Frame
path_frame="C:/Users/anama/OneDrive/Ambiente de Trabalho/UNI/Semestre2/ICSTS/Task3/ICSTS_EIT_Processment/set_01/trial_02/frame_004.png"
image = cv2.imread(path_frame)


## Selecionar manualmente RoI Pulmão Esquerdo
#r_left=cv2.selectROI("select the area left", image)
#cv2.destroyWindow("select the area left")

## Selecionar manualmente RoI Pulmão Direito
#r_right=cv2.selectROI("select the area right", image)
#cv2.destroyWindow("select the area right")

r_left=220, 169, 194, 339 # Coordenadas obtidas com zona anterior comentada
r_right=498, 169, 194, 339

# Representação da zona RoI do pulmão esquero
r=r_left
image_with_roi = image.copy()
cv2.rectangle(image_with_roi, (r[0], r[1]), (r[0] + r[2], r[1] + r[3]), (0, 0, 255), 2)  # Criar rectangulo vermelho

cv2.imshow("Image with ROI", image_with_roi)
cv2.waitKey(0)
cv2.destroyWindow("Image with ROI")

# Abrir e Ler todos os Frames

for set in range(1,5):

    path_file="C:/Users/anama/OneDrive/Ambiente de Trabalho/UNI/Semestre2/ICSTS/Task3/imgs/set_0"+str(set)

    # Lista tudo que está na pasta
    items = os.listdir(path_file)

    # Filtra apenas as pastas
    files_num = len([item for item in items if os.path.isdir(os.path.join(path_file, item))])
        




