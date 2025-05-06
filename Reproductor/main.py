from tkinter import *
import pygame
import os
from tkinter import filedialog
from mutagen.mp3 import MP3
from tkinter import ttk

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
        self.is_paused = False
        self.duracion_total = 0

        pygame.mixer.init()

        self.root.title("Reproductor de Música")
        self.root.geometry("1280x720")
        self.root.configure(bg="#0b0b2a")

        # Frame para la lista de canciones
        self.lista_frame = Frame(self.root)
        self.lista_frame.pack(side=LEFT, padx=0, pady=0, fill=Y)

        self.lista_box = Listbox(self.lista_frame, width=35, height=20, bg="#222241", fg="#4d4d87", font=("Helvetica", 11), justify="center", border= -1)
        self.lista_box.bind('<Double-Button-1>', self.reproducir_seleccionada)
        self.lista_box.pack(side=LEFT, fill=BOTH, expand=True)

        self.menu_contextual = Menu(self.root, tearoff=0)
        self.menu_contextual.add_command(label="Editar", command=self.editar_cancion)
        self.menu_contextual.add_command(label="Eliminar", command=self.eliminar_cancion)
        self.lista_box.bind("<Button-3>", self.mostrar_menu_contextual)

        # Frame central para botones y etiquetas de información
        self.center_frame = Frame(self.root, bg="#0b0b2a")
        self.center_frame.pack(side=TOP, fill=BOTH, expand=True)

        # Frame para controles (botones) centrados
        self.control_frame = Frame(self.center_frame, bg="#0b0b2a")
        self.control_frame.pack(pady=20)

        # Cargar imágenes para los botones
        self.reproducir_img = PhotoImage(file="Reproductor/reproducir.png")
        self.pausar_img = PhotoImage(file="Reproductor/pausa.png")
        self.siguiente_img = PhotoImage(file="Reproductor/siguiente.png")
        self.anterior_img = PhotoImage(file="Reproductor/anterior.png")
        self.agregar_img = PhotoImage(file="Reproductor/examinar.png")

        self.reproducir_btn = Button(self.control_frame, image=self.reproducir_img, command=self.reproducir, bg="#0b0b2a", borderwidth=0)
        self.pausar_btn = Button(self.control_frame, image=self.pausar_img, command=self.pausar, bg="#0b0b2a", borderwidth=0)
        self.siguiente_btn = Button(self.control_frame, image=self.siguiente_img, command=self.siguiente, bg="#0b0b2a", borderwidth=0)
        self.anterior_btn = Button(self.control_frame, image=self.anterior_img, command=self.anterior, bg="#0b0b2a", borderwidth=0)
        self.agregar_btn = Button(self.control_frame, image=self.agregar_img, command=self.agregar_cancion, bg="#0b0b2a", borderwidth=0)

        self.reproducir_btn.grid(row=0, column=0, padx=10)
        self.pausar_btn.grid(row=0, column=1, padx=10)
        self.siguiente_btn.grid(row=0, column=2, padx=10)
        self.anterior_btn.grid(row=0, column=3, padx=10)
        self.agregar_btn.grid(row=0, column=4, padx=10)

        # Etiquetas de canción centradas debajo de botones
        self.info_label = Label(self.center_frame, text="", bg="#0b0b2a", fg="#ff5757", font=("Helvetica", 14))
        self.info_label.pack(pady=(10,0))
        self.info_label2 = Label(self.center_frame, text="", bg="#0b0b2a", fg="#a6a6a6", font=("Helvetica", 11))
        self.info_label2.pack()

        # Frame para barra de progreso y etiquetas de tiempo al fondo
        self.bottom_frame = Frame(self.root, bg="#0b0b2a")
        self.bottom_frame.pack(side=BOTTOM, fill=X, pady=10)

        estilo1 = ttk.Style()
        estilo1.theme_use('clam')
        estilo1.configure("Horizontal.TProgressbar", foreground='white', background='white', troughcolor='#373747',
                          bordercolor='#0b0b2a', lightcolor='white', darkcolor='white')

        # Barra de progreso
        self.progress = ttk.Progressbar(self.bottom_frame, orient=HORIZONTAL, length=500, mode='determinate', style="Horizontal.TProgressbar")
        self.progress.pack(pady=(0,5))

        # Frame para etiquetas de tiempo, lado izquierdo y derecho debajo barra de progreso
        self.tiempos_frame = Frame(self.bottom_frame, bg="#0b0b2a")
        self.tiempos_frame.pack(fill=X)

        self.tiempo_actual_label = Label(self.tiempos_frame, text="00:00", bg="#0b0b2a", fg="white", font=("Helvetica", 10))
        self.tiempo_actual_label.pack(side=LEFT, padx=(20, 0))

        self.tiempo_restante_label = Label(self.tiempos_frame, text="00:00", bg="#0b0b2a", fg="white", font=("Helvetica", 10))
        self.tiempo_restante_label.pack(side=RIGHT, padx=(0, 20))

        self.cargar_canciones()

    def agregar_cancion(self):
        file_path = filedialog.askopenfilename(title="Seleccionar Canción", filetypes=(("MP3 Files", "*.mp3"), ("All Files", "*.*")))
        if file_path:
            nombre_cancion = os.path.basename(file_path)
            artista = "Artista desconocido"
            duracion = "0:00"
            nueva_cancion = Cancion(nombre_cancion, artista, duracion, file_path)
            self.lista_reproduccion.insertar(nueva_cancion)
            self.lista_box.insert(END, f"{nombre_cancion} - {artista}")

    def cargar_canciones(self):
        canciones = [
            Cancion("Down Under", "Men At Work", "3:42", 'Reproductor/DownUnder.mp3'),
            Cancion("Blondie", "Sunset Sons", "3:24", 'Reproductor/Blondie.mp3')
        ]
        for cancion in canciones:
            self.lista_reproduccion.insertar(cancion)
            self.lista_box.insert(END, f"{cancion.nombre} - {cancion.artista}")
        self.nodo_actual = self.lista_reproduccion.cabeza

    def reproducir(self):
        if self.nodo_actual:
            self.cancion_actual = self.nodo_actual.cancion
            if self.is_paused:
                pygame.mixer.music.unpause()
                self.is_paused = False
                self.actualizar_barra()
            else:
                pygame.mixer.music.load(self.cancion_actual.ruta_archivo)
                pygame.mixer.music.play()
                audio = MP3(self.cancion_actual.ruta_archivo)
                self.duracion_total = audio.info.length
                self.progress['maximum'] = self.duracion_total
                self.progress['value'] = 0  # Resetea la barra
                self.info_label.config(text=self.cancion_actual.nombre)
                self.info_label2.config(text=self.cancion_actual.artista)
                self.actualizar_barra()

    def pausar(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.is_paused = True

    def siguiente(self):
        if self.nodo_actual:
            self.nodo_actual = self.lista_reproduccion.obtener_siguiente(self.nodo_actual)
            self.reproducir()

    def anterior(self):
        if self.nodo_actual:
            self.nodo_actual = self.lista_reproduccion.obtener_anterior(self.nodo_actual)
            self.reproducir()

    def reproducir_seleccionada(self, event):
        seleccion = self.lista_box.curselection()
        if seleccion:
            index = seleccion[0]
            self.nodo_actual = self.lista_reproduccion.cabeza
            for _ in range(index):
                self.nodo_actual = self.nodo_actual.siguiente
            self.reproducir()

    def mostrar_menu_contextual(self, event):
        try:
            index = self.lista_box.nearest(event.y)
            self.lista_box.selection_clear(0, END)
            self.lista_box.selection_set(index)
            self.lista_box.activate(index)
            self.menu_contextual.post(event.x_root, event.y_root)
        except:
            pass

    def editar_cancion(self):
        seleccion = self.lista_box.curselection()
        if not seleccion:
            return
        index = seleccion[0]

        nodo = self.lista_reproduccion.cabeza
        for _ in range(index):
            nodo = nodo.siguiente

        ventana = Toplevel(self.root)
        ventana.title("Editar Canción")

        Label(ventana, text="Nombre:").grid(row=0, column=0)
        entrada_nombre = Entry(ventana, width=40)
        entrada_nombre.grid(row=0, column=1)
        entrada_nombre.insert(0, nodo.cancion.nombre)

        Label(ventana, text="Artista:").grid(row=1, column=0)
        entrada_artista = Entry(ventana, width=40)
        entrada_artista.grid(row=1, column=1)
        entrada_artista.insert(0, nodo.cancion.artista)

        def guardar():
            nodo.cancion.nombre = entrada_nombre.get()
            nodo.cancion.artista = entrada_artista.get()
            self.lista_box.delete(index)
            self.lista_box.insert(index, f"{nodo.cancion.nombre} - {nodo.cancion.artista}")
            self.info_label.config(text=self.cancion_actual.nombre)
            self.info_label2.config(text=self.cancion_actual.artista)
            ventana.destroy()

        Button(ventana, text="Guardar", command=guardar).grid(row=2, column=1, pady=10)

    def eliminar_cancion(self):
        seleccion = self.lista_box.curselection()
        if not seleccion:
            return
        index = seleccion[0]

        self.lista_box.delete(index)

        # Eliminar de la lista enlazada
        if self.lista_reproduccion.esta_vacia():
            return

        nodo = self.lista_reproduccion.cabeza
        for _ in range(index):
            nodo = nodo.siguiente

        if nodo == self.lista_reproduccion.cabeza and nodo == self.lista_reproduccion.cola:
            self.lista_reproduccion.cabeza = None
            self.lista_reproduccion.cola = None
        else:
            nodo.anterior.siguiente = nodo.siguiente
            nodo.siguiente.anterior = nodo.anterior
            if nodo == self.lista_reproduccion.cabeza:
                self.lista_reproduccion.cabeza = nodo.siguiente
            if nodo == self.lista_reproduccion.cola:
                self.lista_reproduccion.cola = nodo.anterior

        if self.nodo_actual == nodo:
            self.nodo_actual = nodo.siguiente if nodo.siguiente != nodo else None

    def actualizar_barra(self):
        if pygame.mixer.music.get_busy() or not self.is_paused:
            posicion = pygame.mixer.music.get_pos() / 1000  # en segundos
            self.progress['value'] = posicion
            # Actualizar etiquetas de tiempo
            tiempo_actual = self.formatear_tiempo(posicion)
            tiempo_restante = self.formatear_tiempo(self.duracion_total - posicion)
            self.tiempo_actual_label.config(text=tiempo_actual)
            self.tiempo_restante_label.config(text=tiempo_restante)
            # Volver a llamar a esta función después de 100 milisegundos
            self.root.after(100, self.actualizar_barra)

    def formatear_tiempo(self, segundos):
        minutos = int(segundos // 60)
        segundos = int(segundos % 60)
        return f"{minutos:02}:{segundos:02}"

# Ejecutar la aplicación
if __name__ == "__main__":
    root = Tk()
    app = ReproductorMusica(root)
    root.mainloop()
