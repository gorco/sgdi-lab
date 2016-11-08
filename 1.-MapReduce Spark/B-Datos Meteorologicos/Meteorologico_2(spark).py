# coding=utf-8

# Este fichero generado para la asignatura SGDI
# Practica 1 MapReduce Y Spark, Ejercicio B.2
# Autores: Antonio Calvo Morata y Carlos Congosto Sandoval

# Antonio Calvo Morata y Carlos Congosto Sandoval declaramos que esta solución es fruto exclusivamente de nuestro
# trabajo personal. No hemos sido ayudados por ninguna otra persona ni hemos obtenido la solución de fuentes externas,
# y tampoco hemos compartido nuestra solución con nadie. Declaramos además que no hemos realizado de manera deshonesta
# ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.

import sys
from pyspark import SparkContext

# Dada una linea del fichero devuelve los valores correspondientes a la fecha y a la bateria
# Devuelve repetido el valor de la bateria para poder trabajar con los valores min, avg y max de manera sencilla en
# la reduceByKey permitiendo que tanto entrada como salida sea del mismo formato
def batteryByDate(x):
    day = x[0].split("/")
    return day[1] + "/" + day[0], (x[8], x[8], x[8], 1)

def getMinMaxSum(x, y):
    maxValue = float(max(float(x[0]), float(y[0])))
    sumValue = float(x[1]) + float(y[1])
    minValue = float(min(float(x[2]), float(y[2])))
    count = float(x[3]) + float(y[3])
    return (maxValue, sumValue, minValue, count)

#Dado una lista de 4 valores [maxValue, sumValue, minValue, numValues] en los que el segundo es una suma y el cuarto un
# contador, devuelve una lista con 3 valores en los que el segundo pasa a ser la media
def calculateAverage(x):
    key = x[0]
    values = x[1]
    return key, dict(max=values[0], avg=float(values[1])/float(values[3]), min=values[2])


# sys.argv debe contener el nombre de fichero a procesar
if len(sys.argv) < 2:
    print "No se ha especificado fichero!"
    exit(-1)

path = sys.argv[1]
for i in range(2, len(sys.argv)):
    path += ","+sys.argv[i]

# 2.- Implementar una tarea Apache Spark que resuelva este problema utilizando transformaciones y acciones sobre RDDs.

# Creamos un contexto local y cargamos el fichero        
sc = SparkContext(master="local")
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

sc.stop()