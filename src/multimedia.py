# !/usr/bin/env python3
# Autor: Hernández Albino Edgar Alejandro
#        Maceda Nazario Luis Martín

# Bibliotecas a utilizar
import pygame 
import threading 
import tkinter as tk
from tkinter import*
import webbrowser
import vlc 
import os 

# Para añadir los encabezados a cada sección
def title(frame, message):
    label = tk.Label(frame, text=message, fg="#E5E8E8", bg="#282A36",  font=("Bebas Kai", 30))
    label.pack()

# Para agregar los servicios a cada sección
def service(frame, img):
    service = tk.Label(frame, image=img)
    service.config(bg="#282A36")
    service.pack(pady=15, padx=15)

# Crea divisiones para la ventana
def frame(parent, wid, relX=0):
    divisor = tk.Frame(parent)
    divisor.place(relx=relX, relwidth=wid, relheight=0.9)
    divisor.config(bg="#282A36")
    return divisor

# Creamos botones asando la raiz y la imagen
def button(frame, img):
    press = tk.Button(frame, image=img, bg="#282A36", activebackground="#F325C1")
    press.pack(padx=10, pady=10)
    return press

# Para añadir la dirección web a cada servicio
def web(url):
    webbrowser.open(url)


# Con este método se busca validar que los archivos de la memoria se encuentren dentro de 
# la lista de extensiones permitidas
def buscar(a,fichero):
    for i in range(len(a)):
        if fichero.endswith(a[i]):# Revisa si el archivo termina con una extensión dada por la lista a y regresa True o False
            return True
    return False

# Revisa el contenido de la ubicación donde se encuentran los archivos de USB disponibles
# Si no hay USB regresa una lista vacía
def encontrar(entrada):
    contenido2=os.listdir('/media/pi/')
    if len(contenido2)==0:
        return contenido2 
    # Si hay USB conectada concatena la ubicación de la carptea con el nombre de la memoria
    contenido=os.listdir('/media/pi/'+contenido2[0])
    arreglo=[]
   # Valida que los documentos de la memria cumplan con la extensión
    for fichero in contenido:
        # Con cada iteración verifica que la ruta + el contenido exista y si es así regresa True
        if os.path.isfile(os.path.join('/media/pi/'+contenido2[0],fichero))and buscar(entrada,fichero):
            arreglo.append(fichero)
    return arreglo

# Creamos una clase para elegir la multimedia en otra ventana
class Ventana2:
    def __init__(self,maestro,elec):
        self.maestro=maestro
        maestro.title("Interfaz Memoria")
        a=[".mp3"] # Extensiones de música válidas
        arr=encontrar(a)
        b=[".mp4"] # Extensiones de vídeo válidas
        arr2=encontrar(b)
        c=[".jpg",".png",".jfif"] # Extensiones de imagen válidas
        arr3=encontrar(c)
                    
        # Si no hay nada en la memoria o no hay memoria entrara al siguiente
        if(len(arr)==0 and len(arr2)==0 and len(arr3)==0):
            self.lab=Label(maestro,text="No hay contenido") # Pone una etiqueta de que no hay contenido
            self.lab.pack()
            # Creamos los botones del menú
            self.salir=Button(maestro,text="#SALIR#",command=self.salir)                              
            self.salir.pack()
        if(len(arr)!=0):
            self.boton=Button(maestro,text="■ MÚSICA ■",command=self.youtube)
            self.boton.pack()
        if(len(arr2)!=0):
            self.boton=Button(maestro,text="■ IMÁGENES ■",command=self.spt)
            self.boton.pack()
        if(len(arr3)!=0):
            self.boton=Button(maestro,text="■ VIDEO ■",command=self.memoria)
            self.boton.pack()

    # Le agregamos la función que ejecutara a cada boton
    def youtube(self):
        self.elec=1
        self.maestro.destroy()
    def spt(self):
        self.elec=2
        self.maestro.destroy()
    def memoria(self):
        self.elec=3
        self.maestro.destroy()
    def regresa(self):
        return self.elec
    def salir(self):
        self.elec=5
        self.maestro.destroy()

# Ventana de audio
class Ventana3:
    def __init__(self,maestro,n):
        self.maestro=maestro
        self.i=0
        self.aux=True
        self.ban=True
        self.n=n
        maestro.title("Reproductor de audio")
        pygame.mixer.music.load(self.n[self.i])# Carga el archivo de audio
        pygame.mixer.music.play()# Se reproduce el archivo cargado

        # Creamos los botones del reproductor 
        self.boton=Button(maestro,text="▌▐",command=self.youtube)
        self.boton.pack()
        self.boton1=Button(maestro,text=">>>",command=self.spt)
        self.boton1.pack()
        self.boton2=Button(maestro,text="<<<",command=self.retro)
        self.boton2.pack()
        self.boton3=Button(maestro,text="#SALIR#",command=self.memoria)
        self.boton3.pack()

    # Función de pausa/play del reproductor
    def youtube(self):
        if(self.ban==True):
            pygame.mixer.music.pause()
            self.ban=False
        else:
            pygame.mixer.music.unpause()
            self.ban=True
    # Carga el audio siguente en la lista 
    def spt(self):
        self.i=self.i+1 
        # Si hay más archivos lo reproduce
        if(self.i<len(self.n)):
            pygame.mixer.music.stop()
            pygame.mixer.music.load(self.n[self.i])
            pygame.mixer.music.play()
        # En caso de que sea el último archivo se reinicia la lista
        else:
            self.i=0
            pygame.mixer.music.stop()
            pygame.mixer.music.load(self.n[self.i])
            pygame.mixer.music.play()
    # Retrocede en la lista de reproducción 
    def retro(self):
        self.i=self.i-1
        # Pasa al archivo anterior
        if(self.i>=0):
            pygame.mixer.music.stop()
            pygame.mixer.music.load(self.n[self.i])
            pygame.mixer.music.play()
        # Si el archivo es el primero de la lista pasa al último
        else:
            self.i=len(self.n)-1
            pygame.mixer.music.stop()
            pygame.mixer.music.load(self.n[self.i])
            pygame.mixer.music.play()
    # Para salir del menú
    def memoria(self):
        self.maestro.destroy()
        self.aux=False
        pygame.mixer.music.stop()
    def devolver(self):
        return self.aux

# Ventana de imagen
class Ventana4:
    def __init__(self,maestro,n):
        self.maestro=maestro
        self.i=0
        self.n=n
        maestro.title("Reproductor de Imagenes")
        self.media=vlc.MediaPlayer(self.n[self.i])
        # Despues de crear la imagen se crean los botones
        self.boton1=Button(maestro,text=">>>",command=self.spt)
        self.boton1.pack()
        self.boton2=Button(maestro,text="<<<",command=self.retro)
        self.boton2.pack()
        self.boton3=Button(maestro,text="#SALIR#",command=self.memoria)
        self.boton3.pack()
    # Pasa a la siguiente imagen en la lista
    def spt(self):
        self.media.stop()
        self.i=self.i+1
        # Carga el siguinete archivo si el tamaño de la lista es mayor al i actual
        if(self.i<len(self.n)):
            self.media=vlc.MediaPlayer(self.n[self.i])
            self.media.play()
        # Se reinicia la lista en caso de que sea el último valor
        else:
            self.i=0
            self.media=vlc.MediaPlayer(self.n[self.i])
            self.media.play()

    # Cambia al archivo anterior en la lista
    def retro(self):
        self.i=self.i-1
        self.media.stop()
        if(self.i>=0):
            self.media=vlc.MediaPlayer(self.n[self.i])
            self.media.play()
        # Si es el último archivo pasa al primero
        else:
            self.i=len(self.n)-1
            self.media=vlc.MediaPlayer(self.n[self.i])
            self.media.play()#
    # Quita el reproductor de imagen 
    def memoria(self):
        self.maestro.destroy()
        self.media.stop()

# Ventana de video
class Ventana5:
    def __init__(self,maestro,n):
        self.maestro=maestro
        self.i=0
        self.aux=True
        self.ban=True
        self.n=n
        maestro.title("Reproductor de video")
        self.media=vlc.MediaPlayer(self.n[self.i])
        self.media.play()
        # Se abre la ventana y comienza la reproducción, ademas se crean los botones
        self.boton1=Button(maestro,text=">>>",command=self.spt)
        self.boton1.pack()
        self.boton2=Button(maestro,text="<<<",command=self.retro)
        self.boton2.pack()
        self.boton4=Button(maestro,text="▌▌",command=self.pausa)
        self.boton4.pack()
        self.boton3=Button(maestro,text="#SALIR#",command=self.memoria)
        self.boton3.pack()
    # Función del botón de pausa
    def pausa(self):
        if(self.ban==True):
            self.media.set_pause(1)
            self.ban=False
        else:
            self.media.play()
            self.ban=True
                        
    # Carga el siguinete vídeo en la lista
    def spt(self):
        self.media.stop()
        self.i=self.i+1
        # Carga el siguiente video 
        if(self.i<len(self.n)):
            self.media=vlc.MediaPlayer(self.n[self.i])
            self.media.play()
        # Reinicia la lista
        else:
            self.i=0
            self.media=vlc.MediaPlayer(self.n[self.i])
            self.media.play()

    # Retrocede en la lista para reproducir el vídeo anterior
    def retro(self):
        self.i=self.i-1
        self.media.stop()
        # Si ha siguiente lo reproduce
        if(self.i>=0):
            self.media=vlc.MediaPlayer(self.n[self.i])
            self.media.play()
        # Si no hay siguiente reinicia la lista
        else:
            self.i=len(self.n)-1
            self.media=vlc.MediaPlayer(self.n[self.i])
            self.media.play()
    def memoria(self):
        self.maestro.destroy()
        self.media.stop()

# Se crea la lista de archivos multimedia leídos
def concatena(n):
    for i in range(len(n)):
        contenido=os.listdir('/media/pi/')
        n[i]="/media/pi/"+contenido[0]+"/"+n[i]
    return n 

# Se cerean hilos para emepezar la carga del archivo siguiente aún cuando la ventana 
# actual este en el loop
def incrementar(num,**datos):
    while (datos['inicio'].devolver()):
        if(pygame.mixer.music.get_busy()==0):
            a=datos['inicio'].devolveri()
            # Se verifica que i no este al final de la lista
            if(a==len(datos['arreglo'])-1):
                a=-1
            a=a+1
            #Se poner el valor de i en el objeto de la clase ventana
            # para que pueda ser usado por los métodos de los botones
            datos['inicio'].poneri(a)
            pygame.mixer.music.load(datos['arreglo'][a])
            pygame.mixer.music.play()

    # Cuando termina un archivo de audio comienza el siguiente en automático
    pygame.mixer.music.stop()
    pygame.mixer.quit()

# Crea una instancia de reproductro de múscia
def audio(a):
    ent=pygame.mixer.init()
    a=[".mp3"]
    arr=encontrar(a)
    root=Tk()
    a=0
    arr=concatena(arr)
    vent=Ventana3(root,arr)
    # Se crea un hilo para reproducir el siguiente audio cuando termine el actual
    inicia=threading.Thread(target=incrementar,args=(2,),kwargs={'inicio':vent,'arreglo':arr})
    inicia.start()
    root.mainloop()

# Crea una ventana y verifica los archivos de imagen permitidos
def imagenes(a):
    a=['.jpg','.png','.jfif']
    arr=encontrar(a)
    root=Tk()
    a=0
    arr=concatena(arr)#Obtiene la lista con las rutas completas de los archivos
    #de las imágenes
    vent=Ventana4(root,arr)
    root.mainloop()
# Crea una ventana y verifica los archivos de video permitidos
def videos(a):
    a=['.mp4']
    arr=encontrar(a)#
    root=Tk()
    a=0
    arr=concatena(arr)
    vent=Ventana5(root,arr)
    root.mainloop()

# Función principal main
def main():
    flag=True
    while(flag):
        # Creando la ventana
        raiz = tk.Tk()
        raiz.title("Centro Multimedia")
        raiz.resizable(width=0, height=0)
        raiz.config(bg="#282A36")
        raiz.geometry("850x800")
        raiz.tk.call('wm', 'iconphoto', raiz._w, tk.PhotoImage(file='/home/pi/Downloads/MultimediaCenter/img/multimedia.png'))

        # Creación del frame principal
        mainFrame = tk.Frame(raiz)
        mainFrame.pack(fill="both", expand="True")
        mainFrame.config(bg="#282A36")

        # ---------- FRAME DE MÚSICA ----------
        musicFrame = frame(mainFrame, 0.4)
        title(musicFrame, "MÚSICA")
        # Agregamos las imagenes para los botones
        spotifyImg = tk.PhotoImage(file="/home/pi/Downloads/MultimediaCenter/img/spotify.png")
        appleImg = tk.PhotoImage(file="/home/pi/Downloads/MultimediaCenter/img/apple.png")
        deezerImg = tk.PhotoImage(file="/home/pi/Downloads/MultimediaCenter/img/deezer.png")
        ymusicImg = tk.PhotoImage(file="/home/pi/Downloads/MultimediaCenter/img/ymusic.png")
    	# Creamos los botones de la sección
        spotify = button(musicFrame, spotifyImg)
        apple = button(musicFrame, appleImg)
        deezer = button(musicFrame, deezerImg)
        ymusic = button(musicFrame, ymusicImg)
        # Agregamos la función a los botones
        spotify.config(command=lambda: web('https://open.spotify.com'))
        apple.config(command=lambda: web('https://music.apple.com/mx/browse'))
        deezer.config(command=lambda: web('https://www.deezer.com/mx/'))
        ymusic.config(command=lambda: web('https://music.youtube.com'))

        # ---------- FRAME DE VIDEO ----------
        videoFrame = frame(mainFrame, 0.4, 0.4)
        title(videoFrame, "VIDEO")
        # Agregamos las imagenes para los botones
        youtubeImg = tk.PhotoImage(file="/home/pi/Downloads/MultimediaCenter/img/youtube.png")
        netflixImg = tk.PhotoImage(file="/home/pi/Downloads/MultimediaCenter/img/netflix.png")
        primeImg = tk.PhotoImage(file="/home/pi/Downloads/MultimediaCenter/img/prime-video.png")
        hboImg = tk.PhotoImage(file="/home/pi/Downloads/MultimediaCenter/img/hbo.png")
        disneyImg = tk.PhotoImage(file="/home/pi/Downloads/MultimediaCenter/img/disney.png")
        crunchyImg = tk.PhotoImage(file="/home/pi/Downloads/MultimediaCenter/img/crunchy.png")
        # Creamos los botones de la sección
        youtube = button(videoFrame, youtubeImg)
        netflix = button(videoFrame, netflixImg)
        prime = button(videoFrame, primeImg)
        hbo = button(videoFrame, hboImg)
        disney = button(videoFrame, disneyImg)
        crunchy = button(videoFrame, crunchyImg)
        # Agregamos la función a los botones
        youtube.config(command=lambda: web('https://www.youtube.com'))
        netflix.config(command=lambda: web('https://www.netflix.com/mx-en/login'))
        prime.config(command=lambda: web('https://www.primevideo.com'))
        hbo.config(command=lambda: web('https://www.hbolatam.com/us/account/login'))
        disney.config(command=lambda: web('https://www.disneyplus.com/login'))
        crunchy.config(command=lambda: web('https://www.crunchyroll.com/es/welcome/login'))

        # ---------- FRAME DE MULTIMEDIA ----------
        multiFrame = frame(mainFrame, 0.2, 0.8)
        title(multiFrame, "MULTIMEDIA")
        # Agregamos las imagenes para los botones
        musicImg = tk.PhotoImage(file="/home/pi/Downloads/MultimediaCenter/img/music.png")
        videoImg = tk.PhotoImage(file="/home/pi/Downloads/MultimediaCenter/img/video.png")
        imagenImg = tk.PhotoImage(file="/home/pi/Downloads/MultimediaCenter/img/imagen.png")
         # Creamos los botones de la sección
        music = button(multiFrame, musicImg)
        video = button(multiFrame, videoImg)
        imagen = button(multiFrame, imagenImg)
        # Agregamos la función a los botones
        music.config(command=lambda: audio(a))
        video.config(command=lambda: videos(a))
        imagen.config(command=lambda: imagenes(a))

        # Creamos variables para la reproducción multimedia
        a=0
        r=[".mp3"]
        arr=encontrar(r)
        b=[".mp4"]
        arr2=encontrar(b)
        c=[".jpg",".png",".jfif"]
        arr3=encontrar(c)
        if len(arr)!=0 and len(arr2)==0 and len(arr3)==0:
            a=1
        elif len(arr)==0 and len(arr2)!=0 and len(arr3)==0:
            a=3
        elif len(arr)==0 and len(arr2)==0 and len(arr3)!=0:
            a=2

# Ejecutamos la función main
if __name__ == "__main__":
	main()