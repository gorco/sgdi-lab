# coding=utf-8

# Este fichero generado para la asignatura SGDI
# Practica 1 MapReduce Y Spark, Ejercicio A.3
# Autores: Antonio Calvo Morata y Carlos Congosto Sandoval

# Antonio Calvo Morata y Carlos Congosto Sandoval declaramos que esta solución es fruto exclusivamente de nuestro
# trabajo personal. No hemos sido ayudados por ninguna otra persona ni hemos obtenido la solución de fuentes externas,
# y tampoco hemos compartido nuestra solución con nadie. Declaramos además que no hemos realizado de manera deshonesta
# ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.

from mrjob.job import MRJob
from operator import itemgetter

# 3.-  Implementar una tarea MapReduce en mrjob que resuelva este problema utilizando las fases mapper y reducer,
# y utilice estructuras estáticas para reducir el número de parejas emitidas.
class MRHappinessStatic(MRJob):

    # Inicializar estructura estática
    def __init__(self, *args, **kwargs):
        super(MRHappinessStatic, self).__init__(*args, **kwargs)
        self.listValues = []

	# Fase MAP (line es una cadena de texto)
    def mapper(self, key, line):
        word = line.split()
        if float(word[2]) < 2.0 and word[4] != "--":
            self.listValues.append((word[0], word[2]))

    def mapper_final(self):
        val = sorted(self.listValues, key=itemgetter(1), reverse=True)
        size = len(val) if len(val) < 5 else 5
        for i in range(0, size):
            yield "uniqueKey", val[i]

	# Fase REDUCE (key es una cadena texto, values un generador de valores)
    def reducer(self, key, values):
        valuesList = list(values)
        valuesList = sorted(valuesList, key=itemgetter(1), reverse=True)
        for i in range(0,5):
            yield valuesList[i]


if __name__ == '__main__':
    MRHappinessStatic.run()
