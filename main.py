import time
inicio = time.time()

from PIL import Image, ImageDraw, ImageFont
import cv2

import ProcesarImg as pi

direc="D:/proyecto\ProyectoVPython\Prot1\ssss/*.jpg"
#pi.procesarTodo(direc)

im_pil=Image.open('D:\proyecto\ProyectoVPython\Prot1\ssss/w_2373_42_5399_6.jpg')
print(pi.procesarImagenPIL(im_pil,100))

#im_cv=cv2.imread('D:\proyecto\ProyectoVPython\Prot1\ssss/w_2373_42_5399_6.jpg')
#pi.procesarImagenCV(im_cv)

fin = time.time() 
print(fin-inicio)
