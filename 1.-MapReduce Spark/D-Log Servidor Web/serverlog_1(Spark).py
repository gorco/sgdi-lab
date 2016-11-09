# coding=utf-8

# Este fichero generado para la asignatura SGDI
# Practica 1 MapReduce Y Spark, Ejercicio D.1
# Autores: Antonio Calvo Morata y Carlos Congosto Sandoval

# Antonio Calvo Morata y Carlos Congosto Sandoval declaramos que esta solución es fruto exclusivamente de nuestro
# trabajo personal. No hemos sido ayudados por ninguna otra persona ni hemos obtenido la solución de fuentes externas,
# y tampoco hemos compartido nuestra solución con nadie. Declaramos además que no hemos realizado de manera deshonesta
# ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.

import sys
from pyspark import SparkContext
from pyspark import AccumulatorParam

# Acumulador personalizado - lista
class ListParam(AccumulatorParam):

    def zero(self, v):
        return []

    def addInPlace(self, acc1, acc2):
        acc1.extend(acc2)
        return acc1

# sys.argv debe contener el nombre de fichero a procesar
if len(sys.argv) < 2:
    print "No se ha especificado fichero!"
    exit(-1)

path = sys.argv[1]
for i in range(2, len(sys.argv)):
    path += ","+sys.argv[i]

sc = SparkContext()
fallos = sc.accumulator([], ListParam())
lines = sc.textFile(path)

def compruebayMapea(x):
    x = x.encode('utf-8')
    aux = x.split('\"')
    if len(aux) == 3:
        words = aux[0].split() + [aux[1]] + aux[2].split()
        if len(words) == 8:  # Si la longitud no es 8 es que el formato es incorrecto
            error = 1 if int(words[6]) >= int(400) else 0;  # Comprobar si es un error 4XX o 5XX
            size = 0 if words[7] == "-" else int(words[7]);  # Comprobar tamaño y si no tiene poner 0
            return words[0], (1, size, error)

    #Si el formato no es correcto lo añadimos al acumulador
    fallos.add([x])

datos = (
    lines.map(compruebayMapea)  # comprobamos el formato de las líneas y guardamos la informacion relevante
        .filter(lambda x: x != None)
        .reduceByKey(lambda x, y: (x[0]+y[0], x[1]+y[1], x[2]+y[2])) # Sumamos peticiones con peticiones, tamaño con
                                                                    # tamaño y errores con errores por clave (url)
)

output = datos.collect()
for o in output:
     print o

#imprimimos el log de fallos
print " \n\n Fallos en el fichero:"
print fallos.value

sc.stop()
