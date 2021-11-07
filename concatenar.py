from PIL import Image, ImageFilter, ImageDraw, ImageFont
import glob
import numpy as np
import cv2

# Características del texto
img = Image.new("RGB", (700, 10))
direc = "D:\proyecto\ProyectoVPython\Prot2 Arabic/*.jpg"
cont=1
hor =False
if hor:
    for file in glob.glob(direc):
        imgAux = Image.open(file)
        anc = imgAux.size[0]

        anc_img = img.size[0]

        fondo = Image.new("RGB", (anc+anc_img, 4600))
        fondo.paste(img, (0, 0))
        fondo.paste(imgAux, (anc_img, 0))
        img = fondo
        if(cont==3):
            break
        cont+=1

    img.save('RES' + str(cont) + '.jpg')
else:
    for file in glob.glob(direc):
        imgAux = Image.open(file)
        alt = imgAux.size[1]

        alt_img = img.size[1]
        if alt + alt_img>6400:
            img.save('RES'+str(cont)+'.jpg')
            img = Image.new("RGB", (700, 10))
            alt_img = img.size[1]

        fondo = Image.new("RGB", (700, alt + alt_img))
        fondo.paste(img, (0, 0))
        fondo.paste(imgAux, (0, alt_img))
        img = fondo
        cont+=1

    img.save('RES' + str(cont) + '.jpg')