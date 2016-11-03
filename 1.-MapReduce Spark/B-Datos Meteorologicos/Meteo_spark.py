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

# sys.argv debe contener el nombre de fichero a procesar
if len(sys.argv) != 3:
    print "Falta algún fichero!"
    exit(-1)

# Creamos un contexto local y cargamos el fichero        
sc = Context()

def function(x):
    day = x[0].split("/")
    return day[1] + "/" + day[0], x[8]


for file in range(1,3):#se recorren todas los argumentos de la llamada
    lines = sc.textFile(sys.argv[file])

    datos = (
        lines.map((lambda x: x.split(',')))  # Dividimos en palabras y aplanamos
            .filter(lambda x: x[0] != "date-time")  # borramos la primera linea
            .map(function)  # nos quedamos con la fecha y la batería
            .groupByKey()#.filter(lambda x: x[0] == "01/2013")
            .sortByKey()#ordenamos por fecha
    )

    output = datos.collect()

    for o in output:
        sumValues = 0
        tam = len(o[1])
        o[1].sort()
        maxValue = o[1][-1]
        minValue = o[1][0]
        for valor in o[1]:
            sumValues+=float(str(valor))



        print o[0], "{'max': ",maxValue,"'avg':", sumValues/tam, "'min':",minValue ,"}"

#datos_min = datos.reduceByKey(lambda x,y: min(x,y))#unimos con la misma clave y nos quedamos con el menor
#datos_max = datos.reduceByKey(lambda x,y: max(x,y))#unimos con la misma clave y nos quedamos con el mayor
# datosFinal = datos.collect()
