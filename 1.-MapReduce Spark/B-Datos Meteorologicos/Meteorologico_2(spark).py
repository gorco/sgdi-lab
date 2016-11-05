# coding=utf-8

# Este fichero generado para la asignatura SGDI
# Practica 1 MapReduce Y Spark
# Autores: Antonio Calvo Morata y Carlos Congosto Sandoval

# Antonio Calvo Morata y Carlos Congosto Sandoval declaramos que esta solución es fruto exclusivamente de nuestro
# trabajo personal. No hemos sido ayudados por ninguna otra persona ni hemos obtenido la solución de fuentes externas,
# y tampoco hemos compartido nuestra solución con nadie. Declaramos además que no hemos realizado de manera deshonesta
# ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.

import sys
import unicodedata
from pysparkling import Context

def batteryByDate(x):
    day = x[0].split("/")
    return day[1] + "/" + day[0], (x[8], x[8], x[8], 1)

def getMinMaxSum(x, y):
    maxValue = float(max(float(x[0]), float(y[0])))
    sumValue = float(x[1]) + float(y[1])
    minValue = float(min(float(x[2]), float(y[2])))
    count = float(x[3]) + float(y[3])
    return (maxValue, sumValue, minValue, count)

def calculateAverage(x):
    key = x[0]
    values = x[1] #(maxValue, sumValue, minValue, numValues)
    return key, dict(max=values[0], avg=float(values[1])/float(values[3]), min=values[2])


# sys.argv debe contener el nombre de fichero a procesar
if len(sys.argv) < 2:
    print "No se ha especificado fichero!"
    exit(-1)

path = sys.argv[1]
for i in range(2, len(sys.argv)):
    path += ","+sys.argv[i]

# Creamos un contexto local y cargamos el fichero        
sc = Context()

lines = sc.textFile(path)

datos = (
    lines.map((lambda x: x.split(',')))  # Dividimos en palabras
        .filter(lambda x: x[0] != "date-time")  # Descartamos la primera linea (nombre de las columnas)
        .map(batteryByDate)  # nos quedamos con la fecha y la batería
        .reduceByKey(getMinMaxSum) # Obtenemos el minimo, el maximo
        .map(calculateAverage)
        .sortByKey()
)

output = datos.collect()

for entry in output:
   print entry[0], entry[1]

