from PIL import Image, ImageFilter, ImageDraw, ImageFont
import glob
import numpy as np
import cv2

#Características del texto
font = ImageFont.truetype("arial.ttf", 22)
a=False
if a:
    img=np.zeros((10,300,1),np.uint8)
    direc="D:/proyecto/ProyectoVPython/Prot1/*.jpg"
    cont=0
    for file in glob.glob(direc):
        imgAux = Image.open(file)
        anc = imgAux.size[0]
        alt = imgAux.size[1]
        
        fondo=Image.new("L", (300, alt+10))
        fondo.paste(imgAux, (0, 0))
        
        draw = ImageDraw.Draw(fondo)
        draw.text((10,alt),'llllll', font=font, fill="green")

        imgCV = np.asarray(fondo)

        img = cv2.vconcat([img, imgCV])
        
    cv2.imwrite('RES.jpg',img)
else:
    img=Image.new("RGB", (300, 10))
    direc="D:/proyecto/ProyectoVPython/Prot1/*.jpg"
    cont=0
    for file in glob.glob(direc):
        imgAux = Image.open(file)
        anc = imgAux.size[0]
        alt = imgAux.size[1]

        alt_img=img.size[1]
        
        fondo=Image.new("RGB", (300, alt+alt_img+10))
        fondo.paste(img, (0, 0))
        fondo.paste(imgAux, (0, alt_img))
        
        draw = ImageDraw.Draw(fondo)
        draw.text((10,alt+alt_img-10),'.....', font=font, fill="white")

        img = fondo
        
    img.save('RESU.jpg')
