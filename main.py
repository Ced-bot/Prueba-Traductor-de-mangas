import time

inicio = time.time()

from PIL import Image, ImageDraw, ImageFont
import cv2

import ProcesarImgV2 as pi

direc = "D:\proyecto\ProyectoVPython\Prot3vArabic\ssss/*.jpg"
#pi.cortarTodasImg(direc)
direc='D:\proyecto\ProyectoVPython\Prot3vArabic\cortes/*.jpg'
#pi.concatenarImagenes(direc)
direc='D:\proyecto\ProyectoVPython\Prot3vArabic\conca/*.jpg'
pi.procesarTodo(direc)

fin = time.time()
print(fin - inicio)
