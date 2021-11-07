# -*- coding: utf-8 -*-
import glob
from PIL import Image, ImageDraw, ImageFont
#funcion procesar todas las imagenes
fileRes="0GrisimgPart00.jpg"
#print(fileRes)
img = Image.open(fileRes)
#img=cv2.imread(fileRes)
########################################3
anc=438
alt=459
tam=[anc,alt]
grupos=[[0, 1, 2, 4, 5, 6, 7, 8, 9], [3], [10, 11, 12, 13, 14, 15, 16]]
bloques=[[23, 25, 181, 149], [28, 238, 70, 283], [203, 95, 324, 195]]
textos = ['El mundo cambiará gracias a mí, y un mundo nuevo se completará gracias a mí. ']
def escTexto(im_pil,tam,textos, bloques,rec=True):
    #tamaño de la imagen original
    anc = im_pil.size[0]
    alt = im_pil.size[1]
    var1=anc/tam[0]
    var2=alt/tam[1]
    #escribir el texto de cada cuadrante
    i=0
    font = ImageFont.truetype("arial.ttf", 20)
    draw = ImageDraw.Draw(im_pil)
    for bl in bloques:
        #colocar los nuevos valores para la posicion en la img original
        bl[0]=bl[0]*var1
        bl[1]=bl[1]*var2
        bl[2]=bl[2]*var1
        bl[3]=bl[3]*var2
        #Variable para escribir el texto
        #colocar figuras sobre el texto anterior
        if rec:
            #datos para el rectangulo
            x=bl[0]
            y=bl[1]
            ubicacionIni = (int(x),int(y))
            x=bl[2]
            y=bl[3]
            ubicacionFin = (int(x),int(y))
            draw.rectangle((ubicacionIni,ubicacionFin), fill="#FFFFFF", outline='white', width=1) 
        else:
            val=20
            #datos para el rectangulo
            x=bl[0]
            y=bl[1]
            if x<0 or y<0:
                val=0
            ubicacionIni = (int(x)-val,int(y)-val)
            x=bl[2]
            y=bl[3]
            ubicacionFin = (int(x)+val,int(y)+val)
            draw.ellipse((ubicacionIni,ubicacionFin), fill ="#FFFFFF", outline ="white", width=1)
        #colocar el texto traducido
        text=""
        linea=""
        numCar=int((bl[2]-bl[0])/10)
        for cad in textos[i].split(" "):
            if (len(linea)+len(cad))<numCar:
                linea+=cad+" "
            else:
                text+=linea+'\n'
                linea=cad+" "
        text+=linea
        draw.text((int(bl[0]+10),int(bl[1])), text, font=font, fill="green")
        i+=1
        #Mostrar imagen
        im_pil.save(str(i)+'aaaa.jpg')
        print("CEDDDDDDDDDDDDDDDD")
def escTexto2(img,tam,textos, bloques,rec=True):
    #tamaño de la imagen original
    anc,alt = img.shape[:2]
    var1=0.95*anc/tam[0]
    var2=1.05*alt/tam[1]
    #escribir el texto de cada cuadrante
    i=0
    draw = ImageDraw.Draw(im_pil)
    for bl in bloques:
        #colocar los nuevos valores para la posicion en la img original
        bl[0]=bl[0]*var1
        bl[1]=bl[1]*var2
        bl[2]=bl[2]*var1
        bl[3]=bl[3]*var2
        #Variable para escribir el texto
        #colocar figuras sobre el texto anterior
        if rec:
            #datos para el rectangulo
            x=bl[0]
            y=bl[1]
            ubicacionIni = (int(x),int(y))
            x=bl[2]
            y=bl[3]
            ubicacionFin = (int(x),int(y))
            cv2.rectangle(img,ubicacionIni,ubicacionFin,(0,0,0),-1)
        else:
            #datos para la elipce
            x=bl[0]+(bl[2]-bl[0])/2
            y=bl[1]+(bl[3]-bl[1])/2
            centro=(int(x),int(y))
            x=bl[2]-bl[0]
            y=bl[3]-bl[1]
            tamaño=(int(y)-50,int(x)-50)
            cv2.ellipse(img, centro, tamaño, 90, 0, 360, (0,0,0), -1)
        #########################
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        im_pil = Image.fromarray(img)
        #colocar el texto sobre las figuras
        font = ImageFont.truetype("arial.ttf", 18)
        #colocar el texto traducido
        draw.text((int(bl[0]),int(bl[1])+20), textos[i], font=font, fill="green")
        i+=1
        #Mostrar imagen
        im_pil.save(str(i)+'aaaa.jpg')
        print("CEDDDDDDDDDDDDDDDD")
escTexto(img,tam,textos,bloques,False)
