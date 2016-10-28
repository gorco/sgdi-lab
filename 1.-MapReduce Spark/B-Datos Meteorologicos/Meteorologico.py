# coding=utf-8

# Este fichero generado para la asignatura SGDI
# Practica 1 MapReduce Y Spark
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

# 3.- Implementar una tarea MapReduce en mrjob que resuelva este problema utilizando las fases mapper, combiner y
# reducer
class MRMeteoOpt(MRJob):

	# Fase MAP (line es una cadena de texto)
    def mapper(self, key, line):
        word = line.split(',')
        if word[0] != 'date-time':
            time = word[0].split('/')
            yield str(time[1]) + '/' + str(time[0]), (word[8], word[8], word[8], 1)

    # Fase COMBINER (key es una cadena texto, values un generador de valores)
    def combiner(self, key, values):
        valuesList = list(values)
        sumValue = 0;
        minValue = sys.maxint;
        maxValue = 0;
        count = 0
        for l in valuesList:
            sumValue += float(l[0])
            count += 1
            minValue = float(l[1]) if float(l[1]) < float(minValue) else float(minValue)
            maxValue = float(l[2]) if float(l[2]) > float(maxValue) else float(maxValue)
        yield key, (sumValue, minValue, maxValue, count)

	# Fase REDUCE (key es una cadena texto, values un generador de valores)
    def reducer(self, key, values):
        valuesList = list(values)
        sumValue = 0;
        minValue = sys.maxint;
        maxValue = 0;
        count = 0
        for l in valuesList:
            sumValue += l[0]
            count += l[3]
            minValue = float(l[1]) if float(l[1]) < float(minValue) else float(minValue)
            maxValue = float(l[2]) if float(l[2]) > float(maxValue) else float(maxValue)

        if float(count) > 0:
            avgValue = float(sumValue)/float(count)
            yield key, dict(max = maxValue, avg = avgValue, min = minValue)


if __name__ == '__main__':
    MRMeteo.run()
    MRMeteoOpt.run()
