# coding=utf-8

# Este fichero generado para la asignatura SGDI
# Practica 1 MapReduce Y Spark, Ejercicio C.3
# Autores: Antonio Calvo Morata y Carlos Congosto Sandoval

# Antonio Calvo Morata y Carlos Congosto Sandoval declaramos que esta solución es fruto exclusivamente de nuestro
# trabajo personal. No hemos sido ayudados por ninguna otra persona ni hemos obtenido la solución de fuentes externas,
# y tampoco hemos compartido nuestra solución con nadie. Declaramos además que no hemos realizado de manera deshonesta
# ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.

from mrjob.job import MRJob
from operator import itemgetter
import sys
import os
import re
from collections import defaultdict

# 3.- IImplementar una tarea MapReduce en mrjob que resuelva este problema utilizando las fases mapper, combiner
# y reducer.
class MRIndice(MRJob):
    MRJob.SORT_VALUES = True

	# Fase MAP (line es una cadena de texto)
    def mapper(self, key, line):
        line=line.replace('\'', ' ') # Eliminamos apostrofes
        words = line.split()
        for word in words:
            word = re.sub(r'(\W)*', '', word) # Obtenemos las palabras sin caracteres extraños

            # Devolvemos la palabra como clave y  y un par 1, nombre del fichero origen
            yield word.lower(), (1, os.environ['mapreduce_map_input_file'])

    # Fase COMBINER (key es una cadena texto, values un generador de valores)
    def combiner(self, key, values):
        valuesList = list(values)
        res = defaultdict(list)
        for v, k in valuesList: res[k].append(v)  # Crea un diccionario en el que la key es el libro y los valores
                                                # una lista de números que indican veces de aparición
        for book in res:
            yield key, (sum(res[book]), book) # Devuelve la palabra y el numero de aparariciones por libro

	# Fase REDUCE (key es una cadena texto, values un generador de valores)
    def reducer(self, key, values):
        valuesList = list(values)
        res = defaultdict(list)
        for v, k in valuesList: res[k].append(v) # Crea un diccionario en el que la key es el libro y los valores
                                                # una lista de números que indican veces de aparición
        sumWordsPerBook = [];
        for book in res:
            sumWordsPerBook.append([book, sum(res[book])]) #Obtiene por libro el número de apariciones total de la palabra

        send = False;
        timesInBook = ""
        for entry in sumWordsPerBook:
            timesInBook += "("+entry[0]+", "+str(entry[1])+")" # Creamos el string de salida (libro, nº apariciones)
            if entry[1] > 20: # Si en algún libro hay más de 20 apariciones de la palabra el resultado hay que mandarlo
                send = True;

        if send:
            yield key, timesInBook

if __name__ == '__main__':
    MRIndice.run()
