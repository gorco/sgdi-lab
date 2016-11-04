# coding=utf-8

# Este fichero generado para la asignatura SGDI
# Practica 1 MapReduce Y Spark, Ejercicio B.1
# Autores: Antonio Calvo Morata y Carlos Congosto Sandoval

# Antonio Calvo Morata y Carlos Congosto Sandoval declaramos que esta solución es fruto exclusivamente de nuestro
# trabajo personal. No hemos sido ayudados por ninguna otra persona ni hemos obtenido la solución de fuentes externas,
# y tampoco hemos compartido nuestra solución con nadie. Declaramos además que no hemos realizado de manera deshonesta
# ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.

from mrjob.job import MRJob
from operator import itemgetter
import sys

# 1.- Implementar una tarea MapReduce en mrjob que resuelva este problema utilizando únicamente las fases mapper y
# reducer
class MRMeteo(MRJob):

	# Fase MAP (line es una cadena de texto)
    def mapper(self, key, line):
        word = line.split(',')
        if word[0] != 'date-time':
            time = word[0].split('/')
            yield str(time[1]) + '/' + str(time[0]), word[8]

	# Fase REDUCE (key es una cadena texto, values un generador de valores)
    def reducer(self, key, values):
        valuesList = list(values)
        maxValue = float(max(map(float,valuesList)))
        minValue = float(min(map(float,valuesList)))
        avgValue = float(sum(map(float,valuesList)))/float(len(valuesList))
        yield key, dict(max = maxValue, avg = avgValue, min = minValue)

if __name__ == '__main__':
    MRMeteo.run()
