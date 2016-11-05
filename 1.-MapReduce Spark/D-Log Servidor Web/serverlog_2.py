# coding=utf-8

# Este fichero generado para la asignatura SGDI
# Practica 1 MapReduce Y Spark, Ejercicio D.2
# Autores: Antonio Calvo Morata y Carlos Congosto Sandoval

# Antonio Calvo Morata y Carlos Congosto Sandoval declaramos que esta solución es fruto exclusivamente de nuestro
# trabajo personal. No hemos sido ayudados por ninguna otra persona ni hemos obtenido la solución de fuentes externas,
# y tampoco hemos compartido nuestra solución con nadie. Declaramos además que no hemos realizado de manera deshonesta
# ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.

from mrjob.job import MRJob
from operator import itemgetter
from collections import defaultdict
import mrjob
import itertools

# 2.- Implementar una tarea MapReduce en mrjob que resuelva este problema utilizando las fases mapper, combiner y
# reducer.
class MRServer(MRJob):
    MRJob.SORT_VALUES = True
    MRJob.INPUT_PROTOCOL =  mrjob.protocol.TextValueProtocol # Solution for reading text files which are mostly ASCII
                                                        # but may have some other bytes of unknown encoding (e.g. logs).

	# Fase MAP (line es una cadena de texto)
    def mapper(self, key, line):
        # Formato linea:URL,-,-,hora, zona horaria, peticion, codigo respuesta, tamaño respuesta
        aux = line.split('\"')
        if len(aux) == 3:
            words = aux[0].split() + [aux[1]] + aux[2].split()
            if len(words) == 8:
                error = 1 if int(words[6]) >= int(400) else 0; # Comprobar si es un error 4XX o 5XX
                size = 0 if words[7] == "-" else int(words[7]); # Comprobar tamaño y si no tiene poner 0
                yield words[0], (1, size, error)

    # Fase COMBINER (key es una cadena texto, values un generador de valores)
    def combiner(self, key, values):
        valuesList = list(values)
        sol = [sum(i) for i in itertools.izip_longest(*valuesList, fillvalue=0)] # Suma los valores de la lista por columnas
                                                                                #[[3,7,2],[1,4,5],[9,8,7]] --> [13,19,14]
                                                                                # 3+1+9=13; 7+4+8=19; 2+5+7=14
        yield key, sol

	# Fase REDUCE (key es una cadena texto, values un generador de valores)
    def reducer(self, key, values):
        valuesList = list(values)
        sol = [sum(i) for i in itertools.izip_longest(*valuesList, fillvalue=0)] # Suma los valores de la lista por columnas
                                                                                #[[3,7,2],[1,4,5],[9,8,7]] --> [13,19,14]
                                                                                # 3+1+9=13; 7+4+8=19; 2+5+7=14
        yield str(key), dict(request=sol[0], size=sol[1], err=sol[2])

if __name__ == '__main__':
    MRServer.run()
