import unittest
import os
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import cv2
import time
import math
import glob
from PIL import Image, ImageDraw, ImageFont
from googletrans import Translator
from os import remove

def traducirImagenes(chrome_driver,fileRes,marcas):
    translator = Translator()
    #cargar todas las imagenes del directorio
    #realizar todo el proceso para cada imagen
    direccion='*.jpg'
    #asd=0
    #se crear el marco donde se escribira el texto
    im_pil = Image.open(fileRes)
    font = ImageFont.truetype("arial.ttf", 20)
    draw = ImageDraw.Draw(im_pil)
    #datos
    mar_num=0
    for file in glob.glob(direccion):
        #colocar la imagen en el lugar que corresponde
        nomImg=file
        pest=chrome_driver.find_element_by_id("ocr-upload-file")
        pest.send_keys(os.getcwd()+'/'+nomImg)

        #time.sleep(5)
        #obtener el tamaño de la imagen
        #imgF=chrome_driver.find_element_by_id("ocr-final-image")
        #anc_sw=int(imgF.get_attribute("width"))
        #alt_sw=int(imgF.get_attribute("height"))

        anc_sw=0
        alt_sw=0
        sty=' none;'
        inicio = time.time()
        time.sleep(1)
        while sty==' none;':
            try:
                imgF=chrome_driver.find_element_by_id("ocr-final-image")
                sty=imgF.get_attribute('style').split(':')[1]
                if(sty!=' none;'):
                    anc_sw=int(imgF.get_attribute("width"))
                    alt_sw=int(imgF.get_attribute("height"))
            except:
                time.sleep(1)
        fin = time.time() 
        print('tiempo de fragmento: '+str(fin-inicio))
        #print(str(anc_sw)+'--'+str(alt_sw))
        ################################################################################################################
        #variables para extraer las caracteristicas
        val=0
        izq=[]
        aba=[]
        anc=[]
        alt=[]
        grupos=[]
        #funciona con:  44-45--
        distBl=45
        #leer los datos de la traduccion
        items = chrome_driver.find_elements_by_class_name("ocr-result-span.ocr-result-raw-span")
        for item in items:
            dat=item.get_attribute("style")
            #######################################################################################################################
            #Aqui comienza el prog
            ped=dat.split(';')
            #Agregar los datos de los bloques
            dat=ped[0].split(':')[1].split('p')[0]
            dat0=float(dat)
            dat=ped[1].split(':')[1].split('p')[0]
            dat1=float(dat)
            dat=ped[2].split(':')[1].split('p')[0]
            dat2=float(dat)
            dat=ped[3].split(':')[1].split('p')[0]
            dat3=float(dat)
            
            xMed=dat0+(dat2/2)
            yMed=dat1+(dat3/2)
            #variable para saber cual es el bloque mas cercano
            masC=-1
            for i in range(val):
                #se valida la distancia del bloque a la del resto
                #se calculara la distancia a cuatro puntos del bloque
                xMedA=izq[i]+(anc[i]/2)
                yMedA=aba[i]
                
                xMedB=izq[i]
                yMedB=aba[i]+(alt[i]/2)  
                
                xMedC=izq[i]+(anc[i]/2)
                yMedC=aba[i]+alt[i]
                
                xMedD=izq[i]+anc[i]
                yMedD=aba[i]+(alt[i]/2)
                
                dis1=math.sqrt((xMed-xMedA)**2+(yMed-yMedA)**2)
                dis2=math.sqrt((xMed-xMedB)**2+(yMed-yMedB)**2)
                dis3=math.sqrt((xMed-xMedC)**2+(yMed-yMedC)**2)
                dis4=math.sqrt((xMed-xMedD)**2+(yMed-yMedD)**2)
                #funciona con: 44, ...,54
                vdis=distBl
                if dis1<vdis or dis2<vdis or dis3<vdis or dis4<vdis:
                    masC=i
                    break
            izq.append(dat0)
            aba.append(dat1)
            anc.append(dat2)
            alt.append(dat3)
            #agregar el bloque a un grupo
            seAg=False
            for bloq in grupos:
                try:
                    if(bloq.index(masC)>-1):
                        bloq.append(val)
                        seAg=True
                except:
                    noHacerNada=-1
            if seAg==False:
                grupos.append([val])
            val+=1
        print(grupos)
        #unir grupos separados
        gr=0
        while gr <(len(grupos)-1):
            #indice de los elementos de un grupo
            elm=0
            while elm < len(grupos[gr]):
                #print(str(grupos[gr][elm])+'val')
                xMed=izq[grupos[gr][elm]]+(anc[grupos[gr][elm]]/2)
                yMed=aba[grupos[gr][elm]]+(alt[grupos[gr][elm]]/2)
                #se seguira la iteracion mietras haya grupos en frente
                j=gr
                while j<(len(grupos)-1):
                    for i in grupos[j+1]:
                        #se valida la distancia del bloque a la del resto
                        #se calculara la distancia a cuatro puntos del bloque
                        xMedA=izq[i]+(anc[i]/2)
                        yMedA=aba[i]

                        xMedB=izq[i]
                        yMedB=aba[i]+(alt[i]/2)  

                        xMedC=izq[i]+(anc[i]/2)
                        yMedC=aba[i]+alt[i]

                        xMedD=izq[i]+anc[i]
                        yMedD=aba[i]+(alt[i]/2)

                        dis1=math.sqrt((xMed-xMedA)**2+(yMed-yMedA)**2)
                        dis2=math.sqrt((xMed-xMedB)**2+(yMed-yMedB)**2)
                        dis3=math.sqrt((xMed-xMedC)**2+(yMed-yMedC)**2)
                        dis4=math.sqrt((xMed-xMedD)**2+(yMed-yMedD)**2)
                        ###########
                        vdis=distBl
                        if dis1<vdis or dis2<vdis or dis3<vdis or dis4<vdis:
                            grupos[gr]=grupos[gr]+grupos[j+1]
                            grupos.pop(j+1)
                            break
                    j+=1
                elm+=1
            gr+=1
        print(grupos)
        ####################################################################################
        #obtener el tamaño de cada grupo de bloques
        def menor(arr,gr):
            men=10000
            for i in gr:
                if arr[i]<men:
                    men=arr[i]
            return men
        def mayor(arr1,arr2,gr):
            may=-10000
            for i in gr:
                if (arr1[i]+arr2[i])>may:
                    may=arr1[i]+arr2[i]
            return may
        #obtener el valor del cuadrante final
        bloques=[]
        for gr in grupos:
            #se determina las dimensiones del cuadrante
            mIzq=int(menor(izq,gr))
            mAba=int(menor(aba,gr))
            mDer=int(mayor(izq,anc,gr))
            mArr=int(mayor(aba,alt,gr))
            bloques.append([mIzq,mAba,mDer,mArr])
        print(bloques)
        #############################################################################################################################
        #se reescala la imagen en base a su tamaño en la pag
        #image = cv2.imread(nomImg)
        #alt_og,anc_og = image.shape[:2]
        #imageOut = cv2.resize(image,(anc_sw,alt_sw), interpolation=cv2.INTER_CUBIC)

        imageOut = Image.open(nomImg)
        imageOut.save('D:/proyecto/ProyectoVPython/Prot1/gris/a'+nomImg)
        anc_og = imageOut.size[0]
        alt_og = imageOut.size[1]

        #se cambia el tamaño de la imagen
        #imageOut=imageOut.resize((anc_sw,alt_sw))
        #imageOut.save('D:/proyecto/ProyectoVPython/Prot1/gris/b'+nomImg)

        #se recortan los grupos de la imagen
        num=0
        #se calcula la proporcion de la imagen original y la del SW
        print(str(anc_og)+"-"+str(alt_og))
        print(str(anc_sw)+"-"+str(alt_sw))
        var1=anc_og/anc_sw
        var2=alt_og/alt_sw
        #escribir el texto de cada cuadrante
        nbres=[]
        for bl in bloques:
            #colocar los nuevos valores, y asegurar la posicion correcta en la img original
            bl[0]=bl[0]*var1
            bl[1]=bl[1]*var2
            bl[2]=bl[2]*var1
            bl[3]=bl[3]*var2

            #se realiza el nuevo corte
            #imageOut2 = imageOut[bl[1]:bl[3],bl[0]:bl[2]]
            area=(bl[0]-10,bl[1]-10,bl[2]+10,bl[3]+10)
            print(area)
            imageOut2 = imageOut.crop(area)
            
            fondo = Image.new('L', (anc_og, alt_og))
            fondo.paste(imageOut2, (0, 0), imageOut2)

            #se traduce la nueva imagen
            nombre='res'+str(num)+'.jpg'
            nbres.append(nombre)
            #cv2.imwrite(nombre,imageOut2)
            fondo.save(nombre)
            fondo.save('D:/proyecto/ProyectoVPython/Prot1/gris/'+str(num)+nomImg)

            #se carga la imagen en el ocr
            pest.send_keys(os.getcwd()+'/'+nombre)

            elem=0
            #contador de segundo pasados
            seg=0
            inicio = time.time()
            while elem==0 and seg<4:
                try:
                    #se imprime el texto de la traduccion
                    elem=chrome_driver.find_element_by_class_name("ocr-result-fulltext-raw")
                    print(seg)
                    #solo dibujar la eipce si hay texto
                    if len(elem.text)>0:
                        resultado=elem.text.replace('\n'," ")
                        #--------------------------------------------------------------
                        #se traduce el texto a español
                        result = translator.translate(resultado, dest='es')
                        #se coloca el texto en la imagen de origen
                        #------------------------------------------------------------------  
                        #Dibujar una figura sobre la imagen original
                        x1=int(bl[0])
                        y1=int(bl[1]+marcas[mar_num])
                        x2=int(bl[2])
                        y2=int(bl[3]+marcas[mar_num])
                        val=20
                        #datos para la elipce
                        ubicacionIni = (x1-val,y1-val)
                        ubicacionFin = (x2+val,y2+val)
                        draw.ellipse((ubicacionIni,ubicacionFin), fill ="#FFFFFF", outline ="white", width=1)
                        #colocar el texto traducido
                        text=""
                        linea=""
                        numCar=int((bl[2]-bl[0])/10)
                        for cad in result.text.split(" "):
                            if (len(linea)+len(cad))<numCar:
                                linea+=cad+" "
                            else:
                                text+=linea+'\n'
                                linea=cad+" "
                        text+=linea
                        draw.text((x1+20,y1), text, font=font, fill="green")
                except:
                    seg+=1
                    time.sleep(1)
            fin = time.time() 
            print('tiempo de bloque: '+str(fin-inicio))
            num+=1
        #se debe destruir las imagenes residuales, para no traer conflictos
        #print('------------------------------------------------')
        nb=True
        while nb:
            try:
                for n in nbres:
                    remove(n)
                #print(file)
                remove(file)
                nb=False
            except:
                time.sleep(1)
        #subir el indice de las marcas
        mar_num+=1
        #print('CEDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD')
    resF=fileRes.split('_')
    im_pil.save('D:/proyecto/ProyectoVPython/Prot1/res/'+resF.pop())
    print("Imagen procesada")
