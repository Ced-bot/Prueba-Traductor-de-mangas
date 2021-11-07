import unittest
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

from PIL import Image, ImageFilter
import numpy as np
import cv2
import glob

import TraducirImag as ti
#funcion procesar todas las imagenes
def procesarTodo(direccion):
	#abrir la pestaña de chrome
	chrome_driver = webdriver.Chrome("chromedriver.exe")
	chrome_driver.get('https://www.synapsoft.co.kr/ocr')
	#leer todas las imagenes
	for file in glob.glob(direccion):
		#print(file)
		im_pil=Image.open(file)
		#se procesa la imagen con su version en pillow
		marcas=procesarImagenPIL(im_pil,145)
		#traducir la hoja del manga
		ti.traducirImagenes(chrome_driver,file,marcas)
	chrome_driver.close() 
	print('fin del programa manito')

def convertirAGris(im,num_comp=140):
	#Obtenemos sus dimensiones 150
	x = im.size[0]
	y = im.size[1]
	#Creamos una nueva imagen con las dimensiones de la imagen anterior
	img2 = Image.new('L', (x, y))
	i = 0
	#eje vertical
	while i < y:
		j = 0
		#valores para determinar los cortes
		esOscura=True
		p=0
		#eje horizontal
		while j < x:
			#Obtenemos el valor RGB de cada pixel
			#print(im.getpixel((i,j)))
			r, g, b = im.getpixel((j,i))
			#Obtenemos su equivalente en la escala de gris
			if r<num_comp and g<num_comp and b<num_comp:
			  p = 0
			else:
			  p=255
			#Ese valor lo convertimos a entero
			gris = p
			pixel = tuple([gris])
			#En la nueva imagen en la posición i, j agregamos el nuevo color 
			img2.putpixel((j,i), pixel)
			j += 1
		i += 1
	return img2
#funcion que procesa una imagen
def procesarImagenPIL(im,num_comp=140):
	#Obtenemos sus dimensiones
	x = im.size[0]
	y = im.size[1]
	#Creamos una nueva imagen con las dimensiones de la imagen anterior
	img2 = Image.new('L', (x, y))
	i = 0
	#Arreglo de valores para los cortes
	cortes=[0]
	marcas=['ini']

	Cons=1
	#eje vertical
	while i < y:
		j = 0
		#valores para determinar los cortes
		esOscura=True
		p=0
		#eje horizontal
		while j < x:
			#Obtenemos el valor RGB de cada pixel
			#print(im.getpixel((i,j)))
			r, g, b = im.getpixel((j,i))
			#Obtenemos su equivalente en la escala de gris
			#funciona con 140---142-----150 135
			
			if r<num_comp and g<num_comp and b<num_comp:
			  p = 0
			else:
			  p=255
			  esOscura=False
			#Ese valor lo convertimos a entero
			gris = p
			pixel = tuple([gris])
			#En la nueva imagen en la posición i, j agregamos el nuevo color 
			img2.putpixel((j,i), pixel)
			j += 1
		#Si la fila es oscura, se agrega el valor para realiar un corte
		if esOscura:
			#Si en valor anterior tambien es un fila oscura, se omite
			if i-Cons != cortes[len(cortes)-1]:
				cortes.append(i)
				marcas.append('fin')
				Cons=1
			else:
				Cons+=1
		else:
			if Cons>1:
				cortes.append(i)
				marcas.append('ini')
				Cons=1
		i += 1
	cortes.append(i-1)
	marcas.append('fin')
	#print(cortes)
	#print(marcas)
	#Se crear copias mas pequeñas sin los bloques oscuros
	num=0
	tam=len(cortes)
	#inidice de la imagen que se guardara
	gua=0
	#Guardamos la imagen
	#img2.save('Gris.jpg')

	#variable donde se almacena la imagen que se cortara
	# convertir imagen pillow a opencv
	#image = np.asarray(img2)
	#listas para almacenar el inicio de los cortes
	cors=[]
	while num < tam-1:
		if marcas[num]=='ini' and marcas[num+1]=='fin':
			#se crea las dimensiones de la nueva imagen
			tx=x
			ty=cortes[num+1]-cortes[num]
			#solo crear la nueva imagen si es mayor a 100 pix.
			if ty>90:
				cors.append(cortes[num])
				#recortar la imagen
				area=(0,cortes[num],tx,cortes[num+1])
				imageOut = img2.crop(area)
				#convertir la imagen a gris
				#imageOut=convertirAGris(imageOut,140)

				#ceros
				ceros=""
				if gua<10:
					ceros="0"
				#se guarda la nueva imagen
				nombre=str(num_comp)+'imgPart'+ceros+str(gua)+'.jpg'
				imageOut.save(nombre)
				gua+=1
		num+=1
	return cors
#funcion que procesa una imagen con open cv
def procesarImagenCV(im_cv):
	#Obtenemos sus dimensiones
	y, x = im_cv.shape[:2]
	#print(str(x)+"--"+str(y))
	#Creamos una nueva imagen con las dimensiones de la imagen anterior
	img2 = np.zeros((y,x,3),np.uint8)
	i = 0
	#Arreglo de valores para los cortes
	cortes=[0]
	marcas=['ini']

	Cons=1
	#eje vertical
	while i < y:
		j = 0
		#valores para determinar los cortes
		esOscura=True
		p=[]
		#eje horizontal
		while j < x:
			#Obtenemos el valor RGB de cada pixel
			rgb = im_cv[i,j]
			#Obtenemos su equivalente en la escala de gris
			#funciona con 140---142-----150 135
			num_comp=150
			if rgb[0]<num_comp and rgb[1]<num_comp and rgb[2]<num_comp:
			  p = [0,0,0]
			else:
			  p=[255,255,255]
			  esOscura=False
			#En la nueva imagen en la posición i, j agregamos el nuevo color 
			img2[i,j]=p
			j += 1
		#Si la fila es oscura, se agrega el valor para realiar un corte
		if esOscura:
			#Si en valor anterior tambien es un fila oscura, se omite
			if i-Cons != cortes[len(cortes)-1]:
				cortes.append(i)
				marcas.append('fin')
				Cons=1
			else:
				Cons+=1
		else:
			if Cons>1:
				cortes.append(i)
				marcas.append('ini')
				Cons=1
		i += 1
	cortes.append(i-1)
	marcas.append('fin')
	#print(cortes)
	#print(marcas)
	#Se crear copias mas pequeñas sin los bloques oscuros
	num=0
	tam=len(cortes)
	#inidice de la imagen que se guardara
	gua=0
	#Guardamos la imagen
	#cv2.imwrite("imgGris.jpg",img2)

	#listas para almacenar el inicio de los cortes
	cors=[]
	while num < tam-1:
		if marcas[num]=='ini' and marcas[num+1]=='fin':
			#se crea las dimensiones de la nueva imagen
			tx=x
			ty=cortes[num+1]-cortes[num]
			#recortar la imagen
			imageOut = img2[0:x,cortes[num]:cortes[num+1]]
			#solo crear la nueva imagen si es mayor a 100 pix.
			if ty>90:
				cors.append(cortes[num])
				#recortar la imagen
				imageOut = img2[cortes[num]:cortes[num+1],0:x]
				#ceros
				ceros=""
				if gua<10:
					ceros="0"
				#se guarda la nueva imagen
				nombre='imgPart'+ceros+str(gua)+'.jpg'
				cv2.imwrite(nombre,imageOut)
				gua+=1
		num+=1
	return cors