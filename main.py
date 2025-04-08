from tkinter import *
import pygame
import os
class Cancion(self, nombre, artista, duracion, ruta_archivo):
    def __init__(self):
        self.nombre = nombre
        self.artista = artista
        self.duracion = duracion
        self.ruta_archivo = ruta_archivo
class NodoCancion (self, cancion):
    def __init__(self):
        self.cancion = cancion
        self.siguiente = None
        self.anterior = None

class ListaReproduccion:
    def __init__(self):
        self.cabeza = None
        self.cola = None
    
    def esta_vacia(self):
        return self.cabeza is None
    
    def insertar_ordenado(self,cancion):
        nuevo_nodo = NodoCancion(cancion)

        if self.esta_vacia():
            self.cabeza = self.cola = nuevo_nodo
            self.cabeza.siguiente = self.cabeza
            self.cabeza.anterior = self.cabeza
            return
        actual = self.cabeza
        while actual.siguiente != self.cabeza and actual.siguiente.dato < dato:
            actual = actual.siguiente

        if actual == self.cabeza and dato < self.cabeza.dato:
            nuevo_nodo.siguiente = self.cabeza
            nuevo_nodo.anterior = self.cola
            self.cabeza.anterior = nuevo_nodo
            self.cola.siguiente = nuevo_nodo
            self.cabeza = nuevo_nodo
        else:
            nuevo_nodo.siguiente = actual.siguiente
            nuevo_nodo.anterior = actual
            actual.siguiente.anterior = nuevo_nodo
            actual.siguiente = nuevo_nodo
            if actual == self.cola:
                self.cola = nuevo_nodo

