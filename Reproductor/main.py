from tkinter import *
import pygame
import os
from tkinter import filedialog

class Cancion:
    def __init__(self, nombre, artista, duracion, ruta_archivo):
        self.nombre = nombre
        self.artista = artista
        self.duracion = duracion
        self.ruta_archivo = ruta_archivo

class NodoCancion:
    def __init__(self, cancion):
        self.cancion = cancion
        self.siguiente = None
        self.anterior = None

class ListaReproduccion:
    def __init__(self):
        self.cabeza = None
        self.cola = None

    def esta_vacia(self):
        return self.cabeza is None

    def insertar(self, cancion):
        nuevo_nodo = NodoCancion(cancion)
        if self.esta_vacia():
            self.cabeza = self.cola = nuevo_nodo
            nuevo_nodo.siguiente = nuevo_nodo.anterior = nuevo_nodo
        else:
            nuevo_nodo.siguiente = self.cabeza
            nuevo_nodo.anterior = self.cola
            self.cola.siguiente = nuevo_nodo
            self.cabeza.anterior = nuevo_nodo
            self.cola = nuevo_nodo

    def obtener_siguiente(self, nodo_actual):
        return nodo_actual.siguiente

    def obtener_anterior(self, nodo_actual):
        return nodo_actual.anterior

class ReproductorMusica:
    def __init__(self, root):
        self.root = root
        self.lista_reproduccion = ListaReproduccion()
        self.cancion_actual = None
        self.nodo_actual = None
        self.is_paused = False  # Track if the music is paused

        pygame.mixer.init()

        self.root.title("Reproductor de Música")
        self.root.geometry("400x200")

        self.control_frame = Frame(self.root)
        self.control_frame.pack()

        self.reproducir_btn = Button(self.control_frame, text="Reproducir", command=self.reproducir)
        self.pausar_btn = Button(self.control_frame, text="Pausar", command=self.pausar)
        self.siguiente_btn = Button(self.control_frame, text="Siguiente", command=self.siguiente)
        self.anterior_btn = Button(self.control_frame, text="Anterior", command=self.anterior)
        self.agregar_btn = Button(self.control_frame, text="Agregar Canción", command=self.agregar_cancion)

        self.reproducir_btn.grid(row=0, column=0, padx=5, pady=5)
        self.pausar_btn.grid(row=0, column=1, padx=5, pady=5)
        self.siguiente_btn.grid(row=0, column=2, padx=5, pady=5)
        self.anterior_btn.grid(row=0, column=3, padx=5, pady=5)
        self.agregar_btn.grid(row=0, column=4, padx=5, pady=5)

        self.cargar_canciones()  # Load songs when initializing

    def agregar_cancion(self):
        file_path = filedialog.askopenfilename(title="Seleccionar Canción", filetypes=(("MP3 Files", "*.mp3"), ("All Files", "*.*")))
        if file_path:
            song_name = os.path.basename(file_path)  
            artist_name = "Unknown Artist"  
            duration = "Unknown Duration"  
            self.lista_reproduccion.insertar(Cancion(song_name, artist_name, duration, file_path))

    def cargar_canciones(self):
        self.lista_reproduccion.insertar(Cancion("Down Under", "Men At Work", "3:42", 'Reproductor/DownUnder.mp3'))
        self.lista_reproduccion.insertar(Cancion("Blondie", "Sunset Sons", "3:24", 'Reproductor/Blondie.mp3'))
        self.nodo_actual = self.lista_reproduccion.cabeza

    def reproducir(self):
        if self.nodo_actual:
            self.cancion_actual = self.nodo_actual.cancion
            if self.is_paused:
                pygame.mixer.music.unpause()
                self.is_paused = False
            else:
                pygame.mixer.music.load(self.cancion_actual.ruta_archivo)
                pygame.mixer.music.play()
                self.is_paused = False

    def pausar(self):
        pygame.mixer.music.pause()
        self.is_paused = True

    def siguiente(self):
        if self.nodo_actual:
            self.nodo_actual = self.lista_reproduccion.obtener_siguiente(self.nodo_actual)
            if self.nodo_actual:
                self.reproducir()

    def anterior(self):
        if self.nodo_actual:
            self.nodo_actual = self.lista_reproduccion.obtener_anterior(self.nodo_actual)
            if self.nodo_actual:
                self.reproducir()

if __name__ == "__main__":
    root = Tk()
    reproductor = ReproductorMusica(root)
    root.mainloop()