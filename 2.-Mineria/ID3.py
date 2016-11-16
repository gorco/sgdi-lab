# coding=utf-8

# Este fichero generado para la asignatura SGDI
# Practica 2, Ejercicio 2.ID3
# Autores: Antonio Calvo Morata y Carlos Congosto Sandoval

# Antonio Calvo Morata y Carlos Congosto Sandoval declaramos que esta solución es fruto exclusivamente de nuestro
# trabajo personal. No hemos sido ayudados por ninguna otra persona ni hemos obtenido la solución de fuentes externas,
# y tampoco hemos compartido nuestra solución con nadie. Declaramos además que no hemos realizado de manera deshonesta
# ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.

import csv

class ID3(object):

    def __init__(self, fichero):
        file = open(fichero, 'r')
        next(file, None)  # ignoramos la línea de cabecera
        fieldNames = ['day', 'season', 'wind', 'rain', 'class']
        reader = csv.DictReader(file, fieldNames)

        days = []  # lista de días
        seasons = []  # lista de estaciones
        winds = []  # lista de viento
        rains = []  # lista de lluvia
        classes = []  # lista de clases
        tuplas = []

        # Recorremos el fichero linea a linea
        for row in reader:
            days.append(row['day'])  # el atributo de la primera columna lo añadimos a días
            seasons.append(row['season'])  # el atributo de la segunda columna lo añadimos a estaciones
            winds.append(row['wind'])  # el atributo de la tercera columna lo añadimos a viento
            rains.append(row['rain'])  # el atributo de la cuarta columna lo añadimos a lluvia
            classes.append(row['class'])  # el atributo de la quinta columnalo añadimos a clases
            for i in range(len(fieldNames)):
                tupla = (row[fieldNames[i]], row['class'])
                tuplas.append(tupla)

        atributos = dict(day=days, season=seasons, wind=winds,
                         rain=rains)  # creamos un diccionario con los datos del fichero


    def clasifica(self, instancia):
        pass
        
        
    def test(self, fichero):
        pass


    def save_tree(self, fichero):
        pass
