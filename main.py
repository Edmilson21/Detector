import cv2
import mediapipe as mp
import math,time

video = cv2.VideoCapture(0,cv2.CAP_DSHOW)
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh()
mp_drawing = mp.solutions.drawing_utils # Dibujando los puntos de la cara
inicio = 0
status = ""

while True:
    check,img = video.read()
    img = cv2.resize(img, (1000,720))
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = faceMesh.process(imgRGB)
    h,w,_ = img.shape # extrayendo las dimenciones de la tela

    if results:  # si results nao estiver vazia
        for face in results.multi_face_landmarks:
            #print(face) # obteniendo informacion de la variable results
            #mp_drawing.draw_landmarks(img,face,mpFaceMesh.FACEMESH_FACE_OVAL) #mapeando la cara

            #Buscando as coordenadas del ojo derecho(palpebra de arriba)
            di1x,di1y = int((face.landmark[159].x)*w),int((face.landmark[159].y)*h) # Extraendo las coordenadas para transformarla,s en pixeles en numeros enteros
            # Buscando as coordenadas del ojo derecho(palpebra de abajo)
            di2x, di2y = int((face.landmark[145].x) * w), int((face.landmark[145].y) * h)

            # Buscando as coordenadas del ojo izquierdo(palpebra de arriba)
            es1x, es1y = int((face.landmark[386].x) * w), int((face.landmark[386].y) * h)  # Extraendo las coordenadas para transformarla,s en pixeles en numeros enteros
            # Buscando as coordenadas del ojo izquierdo(palpebra de abajo)
            es2x, es2y = int((face.landmark[374].x) * w), int((face.landmark[374].y) * h)

            #visualizando
            cv2.circle(img, (di1x,di1y),1,(255,0,0),2)
            cv2.circle(img, (di2x, di2y), 1,(255, 0, 0), 2)
            cv2.circle(img, (es1x, es1y), 1,(255, 0, 0), 2)
            cv2.circle(img, (es2x, es2y), 1,(255, 0, 0), 2)

            #Buscando la distancia entre los puntos(ojos)

            distDi= math.hypot(di1x-di2x,di1y-di2y)
            distEs = math.hypot(es1x-es2x,es1y-es2y)
            #print(distDi,distEs)

            if distDi <=8 and distEs <=8:
                #print('Ojos Cerrados')
                cv2.rectangle(img,(100,30),(390,80),(0,0,255),-1)
                cv2.putText(img,"OJOS CERRADOS",(105,65),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),3)
                situacao = "F"
                if situacao!=status:
                    inicio = time.time()
            else:
                #print('Ojos Abiertos')
                cv2.rectangle(img, (100, 30), (390, 80), (0, 255, 0), -1)
                cv2.putText(img, "OJOS ABIERTOS", (105, 65), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)
                situacao = "A"
                inicio = time.time()
                tempo = int(time.time()-inicio)
            if situacao == 'F':
                tempo = int(time.time()-inicio)

            status = situacao

            if tempo >= 2:
                cv2.rectangle(img,(300,150),(850,220),(0,0,255),-1)
                cv2.putText(img,f'DORMINDO {tempo} SEGUNDO(S)',(220,200),cv2.FONT_HERSHEY_SIMPLEX,1.7,(255,255,255),2)
            print(tempo)

    cv2.imshow('IMG',img)
    cv2.waitKey(1)