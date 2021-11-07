from PIL import Image, ImageFilter
import numpy as np
import cv2
import glob
#funcion procesar todas las imagenes
def unirImag(direccion):
	#leer todas las imagenes
	images=[]
	nombres=[]
	for file in glob.glob(direccion):
		#print(file)
		nombres.append(file)
		img=cv2.imread(file)
		images.append(img)
	print(len(images))
	concat_vertical = cv2.vconcat(images[0:10])
	cv2.imwrite('ZZZZZZ.jpg',concat_vertical)
direc="D:\proyecto\ProyectoVPython\Prot1\Ep.41 - 42 DEAD LIFE_files/*.jpg"
unirImag(direc)
print('fin del programa manito')
