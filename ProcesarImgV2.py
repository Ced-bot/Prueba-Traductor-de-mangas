import time
import unittest
from selenium.webdriver.common.keys import Keys
import os
from selenium import webdriver
from PIL import Image, ImageDraw, ImageFont,ImageFilter
import numpy as np
import cv2
import glob
import math
import easyocr

from textblob import TextBlob
from googletrans import Translator
translator = Translator()

#funcion procesar todas las imagenes
def procesarTodo(direccion):
    chrome_driver = webdriver.Chrome("chromedriver.exe")
    chrome_driver.get('https://www.ocrnow.com/extract-Arabic-text-from-Images-or-documents-free-Arabic-ocr-service')
    #cargar easyOCR con arabico
    reader = easyocr.Reader(['ar'])
    #leer todas las imagenes
    for file in glob.glob(direccion):
        inicio = time.time()
        print(file)
        im_pil=Image.open(file)
        #se obtienen los datos de la imagen
        datos = reader.readtext(im_pil)
        #traducir la hoja del manga
        traducirImagenes(datos,im_pil,file,chrome_driver)
        #regresar a la ventana anterior
        chrome_driver.back()
        fin = time.time()
        print('la imagen se proceso en: ',fin - inicio)
    print('fin del programa manito')
#funcion cortar las imagenes para tener menos q procesar
def cortarTodasImg(direccion):
	#leer todas las imagenes
	for file in glob.glob(direccion):
		#print(file)
		im_pil=Image.open(file)
		num=file.split('\\').pop()
		num=num.split('.')[0]
		if int(num)<10:
			num='0'+num
		#se cortan todas las imagenes
		cortarImagenesPIL(im_pil,num)
	print('fin del programa manito')
#concatenar todas las imagenes
def concatenarImagenes(direccion):
	#se crear la imagen base
	img = Image.new("RGB", (700, 1))
	#se procesa cada imagen cortada
	cont = 1
	for file in glob.glob(direccion):
		imgAux = Image.open(file)
		alt = imgAux.size[1]

		alt_img = img.size[1]
		#se guarda la imagene si se excedio el tamaño preestablecido
		if alt + alt_img > 6400:
			img.save('D:\proyecto\ProyectoVPython\Prot3vArabic\conca/RES' + str(cont) + '.jpg')
			img = Image.new("RGB", (700, 1))
			alt_img = img.size[1]
			cont += 1
		#se crea el fondo donde se pegaran las imagenes
		fondo = Image.new("RGB", (700, alt + alt_img))
		fondo.paste(img, (0, 0))
		fondo.paste(imgAux, (0, alt_img))
		img = fondo
	#se guarda el resultado final
	img.save('D:\proyecto\ProyectoVPython\Prot3vArabic\conca/RES' + str(cont) + '.jpg')
#funcion que corta todas la imagenes
def cortarImagenesPIL(im,num_img):
	#Obtenemos sus dimensiones
	x = im.size[0]
	y = im.size[1]
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
		#eje horizontal
		while j < x:
			#Obtenemos el valor RGB de cada pixel
			#print(im.getpixel((i,j)))
			r, g, b = im.getpixel((j,i))
			#Obtenemos su equivalente en la escala de gris
			#funciona con 140---142-----150 135
			if r>10 and g>10 and b>10:
			  esOscura=False
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
	#im.save('NoGris.jpg')

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
			if ty>0:
				cors.append(cortes[num])
				#recortar la imagen
				area=(0,cortes[num],tx,cortes[num+1])
				imageOut = im.crop(area)
				#convertir la imagen a gris
				#imageOut=convertirAGris(imageOut,140)

				#ceros
				ceros=""
				if gua<10:
					ceros="0"
				#se guarda la nueva imagen
				nombre=num_img+'imgPart'+ceros+str(gua)+'.jpg'
				imageOut.save('D:\proyecto\ProyectoVPython\Prot3vArabic\cortes/'+nombre)
				gua+=1
		num+=1
	return cors
#funcion para traducir las imagenes
def traducirImagenes(datos,im_pil,fileRes,chrome_driver):
    # variables para extraer las caracteristicas
    val = 0
    izq = []
    aba = []
    anc = []
    alt = []
    grupos = []
    # funciona con:  44-45--
    distBl = 60
    # leer los datos de la traduccion
    for dato in datos:
        # Agregar los datos de los bloques
        p1,p2,p3,p4=dato[0]
        dat0 = p1[0]
        dat1 = p1[1]
        dat2 = p3[0]-p1[0]
        dat3 = p3[1]-p1[1]

        xMed = dat0 + (dat2 / 2)
        yMed = dat1 + (dat3 / 2)
        # variable para saber cual es el bloque mas cercano
        masC = -1
        for i in range(val):
            # se valida la distancia del bloque a la del resto
            # se calculara la distancia a cuatro puntos del bloque
            xMedA = izq[i] + (anc[i] / 2)
            yMedA = aba[i]

            xMedB = izq[i]
            yMedB = aba[i] + (alt[i] / 2)

            xMedC = izq[i] + (anc[i] / 2)
            yMedC = aba[i] + alt[i]

            xMedD = izq[i] + anc[i]
            yMedD = aba[i] + (alt[i] / 2)

            dis1 = math.sqrt((xMed - xMedA) ** 2 + (yMed - yMedA) ** 2)
            dis2 = math.sqrt((xMed - xMedB) ** 2 + (yMed - yMedB) ** 2)
            dis3 = math.sqrt((xMed - xMedC) ** 2 + (yMed - yMedC) ** 2)
            dis4 = math.sqrt((xMed - xMedD) ** 2 + (yMed - yMedD) ** 2)
            # funciona con: 44, ...,54
            vdis = distBl
            if dis1 < vdis or dis2 < vdis or dis3 < vdis or dis4 < vdis:
                masC = i
                break
        izq.append(dat0)
        aba.append(dat1)
        anc.append(dat2)
        alt.append(dat3)
        # agregar el bloque a un grupo
        seAg = False
        for bloq in grupos:
            try:
                if (bloq.index(masC) > -1):
                    bloq.append(val)
                    seAg = True
            except:
                noHacerNada = -1
        if seAg == False:
            grupos.append([val])
        val += 1
    #print(grupos)
    # unir grupos separados
    gr = 0
    while gr < (len(grupos) - 1):
        # indice de los elementos de un grupo
        elm = 0
        while elm < len(grupos[gr]):
            # print(str(grupos[gr][elm])+'val')
            xMed = izq[grupos[gr][elm]] + (anc[grupos[gr][elm]] / 2)
            yMed = aba[grupos[gr][elm]] + (alt[grupos[gr][elm]] / 2)
            # se seguira la iteracion mietras haya grupos en frente
            j = gr
            while j < (len(grupos) - 1):
                for i in grupos[j + 1]:
                    # se valida la distancia del bloque a la del resto
                    # se calculara la distancia a cuatro puntos del bloque
                    xMedA = izq[i] + (anc[i] / 2)
                    yMedA = aba[i]

                    xMedB = izq[i]
                    yMedB = aba[i] + (alt[i] / 2)

                    xMedC = izq[i] + (anc[i] / 2)
                    yMedC = aba[i] + alt[i]

                    xMedD = izq[i] + anc[i]
                    yMedD = aba[i] + (alt[i] / 2)

                    dis1 = math.sqrt((xMed - xMedA) ** 2 + (yMed - yMedA) ** 2)
                    dis2 = math.sqrt((xMed - xMedB) ** 2 + (yMed - yMedB) ** 2)
                    dis3 = math.sqrt((xMed - xMedC) ** 2 + (yMed - yMedC) ** 2)
                    dis4 = math.sqrt((xMed - xMedD) ** 2 + (yMed - yMedD) ** 2)
                    ###########
                    vdis = distBl
                    if dis1 < vdis or dis2 < vdis or dis3 < vdis or dis4 < vdis:
                        grupos[gr] = grupos[gr] + grupos[j + 1]
                        grupos.pop(j + 1)
                        break
                j += 1
            elm += 1
        gr += 1
    #print(grupos)

    ####################################################################################
    # obtener el tamaño de cada grupo de bloques
    def menor(arr, gr):
        men = 10000
        for i in gr:
            if arr[i] < men:
                men = arr[i]
        return men

    def mayor(arr1, arr2, gr):
        may = -10000
        for i in gr:
            if (arr1[i] + arr2[i]) > may:
                may = arr1[i] + arr2[i]
        return may

    # obtener el valor del cuadrante final
    bloques = []
    for gr in grupos:
        # se determina las dimensiones del cuadrante
        mIzq = int(menor(izq, gr))
        mAba = int(menor(aba, gr))
        mDer = int(mayor(izq, anc, gr))
        mArr = int(mayor(aba, alt, gr))
        bloques.append([mIzq, mAba, mDer, mArr])
    #print(bloques)
    ##############################################################################################
    # cortar el texto de cada cuadrante
    #imagen base para concatenar los bloques
    img = Image.new("RGB", (300, 10))
    font = ImageFont.truetype("arial.ttf", 22)
    for bl in bloques:
        # se realiza el nuevo corte
        area = (bl[0] - 10, bl[1] - 10, bl[2] + 10, bl[3] + 10)
        #print(area)
        imgAux = im_pil.crop(area)

        # colocar un piltro difuso en la imagen
        imgAux = imgAux.filter(ImageFilter.DETAIL)
        #imgAux = imgAux.filter(ImageFilter.EDGE_ENHANCE)

        #se concatenan los bloques
        anc=imgAux.size[0]
        alt = imgAux.size[1]
        if anc<img.size[0]:
            anc = img.size[0]
        alt_img = img.size[1]
        #se crea un nueo fondo donde se agruparan las dos imagenes
        fondo = Image.new("RGB", (anc, alt + alt_img + 20))
        fondo.paste(img, (0, 0))
        fondo.paste(imgAux, (0, alt_img))
        #se coloca el texto separador
        draw = ImageDraw.Draw(fondo)
        draw.text((10, alt + alt_img - 5), 'uwu', font=font, fill="white")
        img = fondo
    resF = fileRes.split('RES')
    nom='RESU'+resF[1]
    img.save(nom)
    # cargar la imagen en la pagina
    chrome_driver.find_element_by_id("single").send_keys(os.getcwd() + '/'+nom)
    # presionar el boton para detectar el texto
    time.sleep(1)
    noCar=True
    while noCar:
        try:
            tab = chrome_driver.find_element_by_tag_name('button')
            tab.click()
            noCar=False
        except:
            print('a')
            time.sleep(1)
    # selecionar el texto de la traduccion
    noCar=True
    text=''
    while noCar:
        try:
            elem = chrome_driver.find_element_by_class_name("Home_code__axx2Y")
            text=elem.text
            noCar=False
        except:
            print('b')
            time.sleep(1)
    #dividir los bloques textos en cada bloque
    textos=text.split('uwu')
    rg=len(textos)//2
    im_pil=Image.open(fileRes)
    draw = ImageDraw.Draw(im_pil)
    for i in range(rg):
        #solo realizar el proceso si hay texto
        blob = TextBlob(textos[i+rg])
        if(len(textos[i+rg])>1 and (blob.detect_language()=='ar' or blob.detect_language()=='sd')):
            # se traduce el texto a español
            #result = blob.translate(to='es')
            result = translator.translate(textos[i+rg], dest='es')
            #print(textos[i+rg])
            # se coloca el texto en la imagen de origen
            # ------------------------------------------------------------------
            # Dibujar una figura sobre la imagen original
            x1 = int(bloques[i][0])
            y1 = int(bloques[i][1])
            x2 = int(bloques[i][2])
            y2 = int(bloques[i][3])
            val = 20
            # datos para la elipce
            ubicacionIni = (x1 - val, y1 - val)
            ubicacionFin = (x2 + val, y2 + val)
            draw.ellipse((ubicacionIni, ubicacionFin), fill="#FFFFFF", outline="white", width=1)
            # colocar el texto traducido
            text = ""
            linea = ""
            numCar = (x2 - x1) // 10
            for cad in result.text.split(" "):
                if (len(linea) + len(cad)) < numCar:
                    linea += cad + " "
                else:
                    text += linea + '\n'
                    linea = cad + " "
            text += linea
            draw.text((x1 + 20, y1), text, font=font, fill="green")
    im_pil.save('D:\proyecto\ProyectoVPython\Prot3vArabic/res/'+resF.pop())