# coding=utf-8

# Este fichero generado para la asignatura SGDI
# Practica 1 MapReduce Y Spark
# Autores: Antonio Calvo Morata y Carlos Congosto Sandoval

# Antonio Calvo Morata y Carlos Congosto Sandoval declaramos que esta solución es fruto exclusivamente de nuestro
# trabajo personal. No hemos sido ayudados por ninguna otra persona ni hemos obtenido la solución de fuentes externas,
# y tampoco hemos compartido nuestra solución con nadie. Declaramos además que no hemos realizado de manera deshonesta
# ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.

import sys
from doctest import _OutputRedirectingPdb

from pysparkling import Context

# sys.argv debe contener el nombre de fichero a procesar
if len(sys.argv) != 3:
    print "Falta algún fichero!"
    exit(-1)

# Creamos un contexto local y cargamos el fichero        
sc = Context()
#list = []

lines = sc.textFile(sys.argv[1])


def function(x):
    day = x[0].split("/")
    return day[1] + "/" + day[0], x[8]





datos = (
    lines.map((lambda x: x.split(',')))  # Dividimos en palabras y aplanamos
        .filter(lambda x: x[0] != "date-time")  # borramos la primera linea
        .map(function)  # nos quedamos con la fecha y la batería
       # .reduceByKey(lambda x,y: (x,y))
        #.flatMap(lambda x: x[1])
)

datos2 = datos.reduceByKey(lambda x: list.append(x))

#cambiar que esto es lo mismo que otro grupo
datos_min = datos.reduceByKey(lambda x,y: min(x,y))
datos_max = datos.reduceByKey(lambda x,y: max(x,y))
datos_avg = datos.reduceByKey(lambda x,y: (x+y))

# En lugar de almacenar en disco, recolectamos y mostramos por pantalla
list = datos2.values()
for l in list:
    print l
#utput = datos.collect()
#print datos_avg.collect()
#for d in list:
 #   print d
#print output
#min = output.min()
# max = output.max()
# print "min: "+ min+ "\t max: "+ max
# sc.stop()
