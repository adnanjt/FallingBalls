
# OpenCV en Python : http://opencv.willowgarage.com/documentation/python/index.html
#http://www.cs.iit.edu/~agam/cs512/lect-notes/opencv-intro/opencv-intro.html
import cv2
import cv2.cv as cv
import random
import mp3play
import time
import numpy as np
from random import randint
cd "C:\Users\Owner\Documents\GitHub\FallingBalls"
ESC = 27 #Valor ASCII de el ESC
portada = cv.LoadImage("PortadaFB.jpg")
def WaitKey(delay = 0):
    c = cv.WaitKey(delay)

    if c == -1:
        ret = -1
    else:
        ret = c & ~0b100000000000000000000 
    return ret

if __name__ == '__main__':
    cv.NamedWindow("Falling Balls", cv.CV_WINDOW_AUTOSIZE)
<<<<<<< HEAD

    cv2.resizeWindow("Falling Balls", 500, 500)

=======

    cv2.resizeWindow("Falling Balls", 500, 500)

>>>>>>> origin/master
    cv.ShowImage("Falling Balls", portada)
    c = cv.WaitKey()
    print "%d - %d" % (c & ~0b100000000000000000000,c)


#Clase para la imagen
#ATRIBUTOS:
#Posiciones en X y Y aleatorias de la imagen
#Velocidad de la bolita 
#Si la bolita esta activa
#METODOS: 
#Obtener la posicion y el shape 
#Obtener el centro u origen 
#Actualizar la posicion con la velocidad
class Bolita:
    """ Clase representando la bolita """
    def __init__(self, x, y, tipo):#constructor de la bolita
        self.x = x
        self.y = y
        self.width = 0
        self.height = 0
        self.speed = (0,1)
        self.active = True
        self.tipo = tipo



    def getDimensions(self):
        return (self.x, self.y, self.width, self.height)

    def centerOrigin(self):
        return (self.x - self.width/2, self.y - self.height/2)

    def update(self):
        self.x += self.speed[0]
        self.y += self.speed[1]




#Creacion de la ventana para mostrar las imagenes capturadas
#cv.NamedWindow("window_a", cv.CV_WINDOW_AUTOSIZE)#Ventana para mostrar el juego
#cv.NamedWindow("window_b", cv.CV_WINDOW_AUTOSIZE)#Ventana para mostrar la diferencia

archivo = r'C:\users\angelo\my documents\Minimal.mp3'#Path del archivo de musica
archivo2 = r'C:\users\angelo\my documents\bolitatocada.mp3'
archivo3 = r'C:\users\angelo\my documents\bombaS.mp3'
archivo4 = r'C:\users\angelo\my documents\GameOver.mp3'
mp3 = mp3play.load(archivo)#Cargar el archivo de musica 
mp32 = mp3play.load(archivo2)
mp33 = mp3play.load(archivo3)
mp34 = mp3play.load(archivo4)


# Estructuracion del elemento para la dilatacion, "ubica y llena el kernel rectangular convolucional" para interactuar con la imagen para los cambios morfologicos
es = cv.CreateStructuringElementEx(9,9, 4,4, cv.CV_SHAPE_ELLIPSE)

# Configuracion de la Webcam
# Usar la camara por default
cam = cv.CaptureFromCAM(-1)# Si esto no funciona intentarlo con 0
# Establecer las dimensiones de los frames obtenidos de la camara para grabar al video
frame_size = (int(cv.GetCaptureProperty(cam, cv.CV_CAP_PROP_FRAME_WIDTH)),int(cv.GetCaptureProperty(cam, cv.CV_CAP_PROP_FRAME_HEIGHT)))

## Configurar el video
# Poner en verdadero en caso que se quiera grabar un video del juego
writeVideo = False

fourcc = cv.FOURCC('M', 'J', 'P', 'G')#codigo de 4 caracteres para los codecs, compresion con MJPEG
fps = 30#frames por segundo del video a escribir
# Creacion del archivo del video
if writeVideo:
    video_writer = cv.CreateVideoWriter("movie.avi", fourcc, fps, frame_size)#Crear el archivo con el nombre "movie.avi"

#Se crean las imagenes del tamanio de los frames a 8 bits con 3 canales
previo = cv.CreateImage(frame_size, 8L, 3)#frame previo
cv.SetZero(previo)#Limpia el arreglo

diferencia = cv.CreateImage(frame_size, 8L, 3)#diferencia de las imagenes para calcular el movimiento
cv.SetZero(diferencia)#Limpia el arreglo

actual = cv.CreateImage(frame_size, 8L, 3)#frame actual
cv.SetZero(actual)#Limpia el arreglo

bola_original = cv.LoadImage("ColoredBall.png")#Cargar la  imagen de la bolita con su numero de bits y canales por pixel
bola = cv.CreateImage((64,64), bola_original.depth, bola_original.channels)
cv.Resize(bola_original, bola)#Pone la bola_original a 64x64

#######################################################################
#######################################################################
#######################################################################
bomba_original = cv.LoadImage("bomba.png")#Cargar la  imagen de la bomba
bomba = cv.CreateImage((64,64), bomba_original.depth, bomba_original.channels)
cv.Resize(bomba_original, bomba)#Pone la bomba_original a 64x64


#######################################################################
#######################################################################
#######################################################################

corazon_original = cv.LoadImage("corazon.png")#Cargar la  imagen de la bolita con su numero de bits y canales por pixel
corazon = cv.CreateImage((64,64), corazon_original.depth, corazon_original.channels)
cv.Resize(corazon_original, corazon)#Pone la bola_original a 64x64

#######################################################################
#######################################################################
#######################################################################

mask_original = cv.LoadImage("input-mask.png")#Cargar la mascara de entrada para la bolita(esto es para descartar el contorno y solo dejar la parte de la bolita)
mask = cv.CreateImage((64,64), mask_original.depth, bola_original.channels)
cv.Resize(mask_original, mask)#Bolita final 


mask_original2 = cv.LoadImage("bomba_mask.png")#Cargar la mascara de entrada para la bolita(esto es para descartar el contorno y solo dejar la parte de la bolita)
mask2 = cv.CreateImage((64,64), mask_original2.depth, bomba_original.channels)
cv.Resize(mask_original2, mask2)#Bolita final 

mask_original3 = cv.LoadImage("corazon_mask.png")#Cargar la mascara de entrada para la bolita(esto es para descartar el contorno y solo dejar la parte de la bolita)
mask3 = cv.CreateImage((64,64), mask_original3.depth, corazon_original.channels)
cv.Resize(mask_original3, mask3)#Bolita final 

def valor_hit(imagen, bolita):
    roi = cv.GetSubRect(imagen, bolita.getDimensions())#se corta la imagen del tamano de la bolita
    return cv.CountNonZero(roi)#numero de elementos que no son cero del arreglo de entrada

#funcion para crear una lista de x bolitas del mismo tamano de la original
def crear_objetos(count):
    #tipo = 0 para la blita, 1 para la bomba
    #Generacion de numero aleatorio de 0 y 1
    tipo = 0
    targets = list()#Lista de las bolitas
    for i in range(count):
        if count > 3:#crear menos bombas que bolitas
<<<<<<< HEAD
            tipo = randint(0, 1)
=======
            tipo = randint(0, 10)#probabilidad mas alta que salga una bolita a una bomba
            if tipo >= 0 and tipo <= 7:
                tipo = 0

            else: 
                tipo=1
>>>>>>> origin/master

        tgt = Bolita(random.randint(0, frame_size[0]-bola.width), 0, tipo)#Limitar las posiciones en x y y que pueda cojer la bolita con su ancho y con el del frame
        tgt.width = bola.width#ancho de la misma imagen original
        tgt.height = bola.height#altura de la misma imagen original
        targets.append(tgt)#agregar a la lista la nueva creada

    return targets#se retorna la lista de las bolitas

def terminar_juego():
#while True:
#capture = cv.QueryFrame(cam)# Capturar un frame de la camara
#frame = cv.CreateImage(frame_size, 8, 1)#creacion del frame
#cv.Flip(capture, capture, flipMode=1)#rotar la imagen para que salga derecha
    c = WaitKey(15000)# Acabar el juego si se presiona ESC
    cv2.destroyAllWindows()
    mp3.stop()

#funcion para crear las vidas a mostrarse e3n pantalla
def crear_vidas(count):
    vidas = list()#Lista de corazones
    posx = 430
    for i in range(count):
        tgt = Bolita(posx, 400, 0)#Limitar las posiciones en x y y que pueda cojer la bolita con su ancho y con el del frame
        tgt.width = corazon.width#ancho de la misma imagen original
        tgt.height = corazon.height#altura de la misma imagen original
        vidas.append(tgt)#agregar a la lista la nueva creada
        posx = posx+70
    return vidas#se retorna la lista de las bolitas

#funcion para detectar la cara y asi delimitar la distancia 
def detect_faces(image):
    faces = []
    detected = cv.HaarDetectObjects(image, cascade, storage, 1.2, 2, cv.CV_HAAR_DO_CANNY_PRUNING, (100,100))
    if detected:
        for (x,y,w,h),n in detected:
            faces.append((x,y,w,h))
    return faces


cascade = cv.Load('haarcascade_frontalface_default.xml')
storage = cv.CreateMemStorage()
nbolas = 5#numero de bolas
targets = crear_objetos(nbolas)

initialDelay = 100 #Retraso inicial

score = 0#puntuacion

font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 8, 8)#Letras para mostrar la puntuacion
font2 = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 4, 8)#Letras para mostrar la puntuacion
font3 = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 8, 8)#Letras para mostrar la puntuacion

nvidas = 3#numero de vidas del jugador
vidas = crear_vidas(nvidas)#crear la lista de corazoncitas

# capture - footage original 
# actual - footage borroso(blurred ), blured para eliminar el ruido
# diferencia - fame de la diferencia
# frame - frame diferenciado gray scaled > threshold(umbral) > dilate | working image (Pata detectar el movimiento), El filtro treshhold para que los pixeles de la diferencia sean blancos 
# bola_original - imagen de la bolaF
# bola - imagen de la bola menor
# mask_original - imagen de mascara
# mask - imagen de mascara menor
juego_terminado = False
<<<<<<< HEAD
=======


>>>>>>> origin/master
# Loop principal
dentroPosicion = True
mp3.play()
i = 0
while juego_terminado == False:
<<<<<<< HEAD
=======
    
>>>>>>> origin/master
    capture = cv.QueryFrame(cam)# Capturar un frame de la camara
    cv.Flip(capture, capture, flipMode=1)#rotar la imagen para que salga derecha
    for v in vidas:
        cv.SetImageROI(capture, v.getDimensions())
        cv.Copy(corazon, capture, mask3)
        cv.ResetImageROI(capture)
    ############################################################3
    if i%5==0:
            faces = detect_faces(capture)
    for (x,y,w,h) in faces:
        cv.Rectangle(capture, (x,y), (x+w,y+h), 255)
        x2 = x 
        w2 = w 
        y2 = y
        h2 = h 
        #print(x+w, y+w)
        if x2+w2 >= 350 and x2+w2 <= 400 and y2+h2>= 350 and y2+h2 <= 400:
            cv.PutText(capture, "                                    " , (50,frame_size[1]-50), font, cv.RGB(100,30,80))
            dentroPosicion = True
        else:
<<<<<<< HEAD
            cv.PutText(capture, "Muevase hacia la posicion de juego: " , (50,frame_size[1]-50), font, cv.RGB(100,30,80))
            actual = previo
            dentroPosicion = False
=======
            cv.PutText(capture, "Muevase hacia la posicion de juego: " , (50,frame_size[1]-100), font, cv.RGB(100,30,80))

    

>>>>>>> origin/master
    ##############################################################
    cv.Smooth(capture, actual, cv.CV_BLUR, 15,15)#suavisado para evitar falsos positivos de la imagen
    cv.AbsDiff(actual, previo, diferencia)# Diferencia entre los frames pixel por pixel
    frame = cv.CreateImage(frame_size, 8, 1)#creacion del frame
    frame_completo = cv.CreateImage((frame.width*2,frame.height), 8, 1) #creacion del frame para ambas imagenes
    cv.CvtColor(diferencia, frame, cv.CV_BGR2GRAY)#convertido a escala de grises
    cv.Threshold(frame, frame, 10, 0xff, cv.CV_THRESH_BINARY)#se le aplica un treshold
    cv.Dilate(frame, frame, element=es, iterations=3)#se dilata con el elemento estructural creado 3 veces sobre la imagen
    if initialDelay <= 0:#cuando se termine el delay
        for t in targets:
            if t.active:
                nzero = valor_hit(frame, t)
                if nzero < 1000:#parametro de decision
                    # Dibujar la bolita en la pantalla
                    cv.SetImageROI(capture, t.getDimensions())#Establecer el ROI (region de interes)
                    if t.tipo == 0:
                        cv.Copy(bola, capture, mask)#si la mascara es diferente de 0 copia en capture la bolita
                    else: 
                        cv.Copy(bomba, capture, mask2)
                    cv.ResetImageROI(capture)#resetear
                    #if dentroPosicion == True:
                    t.update()#actualizar posicion, vel
                    # En caso que la bolita llegue al final de la pantalla 
                    if t.y + t.height >= frame_size[1]:
                        if t.tipo ==0:
                            t.active = False
                            nbolas -= 1
<<<<<<< HEAD
=======

>>>>>>> origin/master
                        else: #en caso de una bomba llegar al final, debe reiniciar
                            tipo = randint(0, 10)#probabilidad mas alta que salga una bolita a una bomba
                            if tipo >= 0 and tipo <= 7:
                                tipo = 0
                            else: 
                                tipo=1
<<<<<<< HEAD
                            t.tipo = tipo
                            t.y = 0#se ubica la bolita al inicio de la pantalla
                            t.x = random.randint(0, frame_size[0]-bola.width)#ubicacion aleatoria en el eje x
                        if nbolas ==0 and nvidas >0: #crear nuevos elementos siempre y cuando resten vidas 
                            nbolas = 5 
                            targets = crear_objetos(nbolas)
=======

                            t.tipo = tipo
                            t.y = 0#se ubica la bolita al inicio de la pantalla
                            t.x = random.randint(0, frame_size[0]-bola.width)#ubicacion aleatoria en el eje x

                        if nbolas ==0 and nvidas >0: #crear nuevos elementos siempre y cuando resten vidas 
                            nbolas = 5 
                            targets = crear_objetos(nbolas)




>>>>>>> origin/master
                else:#eliminar una bolita si la mano ocupa el cuadro de una bolita(vuelve al inicio)
                    
                    if t.tipo == 0:
                        mp32.play()
                    else: 
                        mp33.play()
                        nvidas-=1 #Para eliminar las vidas de la pantalla
                        vidas = crear_vidas(nvidas)
                        if nvidas<0:
                            juego_terminado = True
                            cv.PutText(capture, "GAME OVER" , (50,frame_size[1]/2), font3, cv.RGB(150,0,0))
                            cv.PutText(capture, "GAME OVER" , (50*5,frame_size[1]/2), font3, cv.RGB(150,0,0))
                            cv.PutText(capture, "GAME OVER" , (50*10,frame_size[1]/2), font3, cv.RGB(150,0,0))
<<<<<<< HEAD
=======
                            mp34.play()
>>>>>>> origin/master
                            break
                    tipoprev = t.tipo
                    tipo = randint(0, 10)#probabilidad mas alta que salga una bolita a una bomba
                    if tipo >= 0 and tipo <= 7:
                        tipo = 0
                    t.tipo = tipo
                    t.y = 0#se ubica la bolita al inicio de la pantalla
                    t.x = random.randint(0, frame_size[0]-bola.width)#ubicacion aleatoria en el eje x
                    if t.speed[1] < 15:#aumento de la velocidad
                        t.speed = (0, t.speed[1]+1)
                    if tipoprev == 0:
                        score += nbolas#sumar el numero de bolas a la puntuacion
<<<<<<< HEAD
    cv.PutText(capture, "Puntuacion: %d" % score, (10,frame_size[1]-10), font2, cv.RGB(0,0,0))#Agregar el titulo del score en pantalla
=======
    
    cv.PutText(capture, "Puntuacion: %d" % score, (10,frame_size[1]-10), font2, cv.RGB(255,200,200))#Agregar el titulo del score en pantalla
>>>>>>> origin/master
    cv.ShowImage("Juego", frame)#Mostrar la ventana del juego
    if writeVideo:
        cv.WriteFrame(video_writer, capture)
    cv.ShowImage("Morfologia", capture)
<<<<<<< HEAD
=======



>>>>>>> origin/master
    previo = cv.CloneImage(actual)#se guarda este frame en para la proxima diferencia
    c = WaitKey(2)# Acabar el juego si se presiona ESC
    if c == 27:
        cv2.destroyAllWindows()
        mp3.stop()
        break
    initialDelay -= 1#ir disminuyendo el delay
    i += 1
terminar_juego()
print score#imprimir el score

<<<<<<< HEAD
terminar_juego()
print score#imprimir el score
=======
>>>>>>> origin/master
