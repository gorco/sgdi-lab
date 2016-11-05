# coding=utf-8

# Este fichero generado para la asignatura SGDI
# Practica 1 MapReduce Y Spark, Ejercicio A.2
# Autores: Antonio Calvo Morata y Carlos Congosto Sandoval

# Antonio Calvo Morata y Carlos Congosto Sandoval declaramos que esta solución es fruto exclusivamente de nuestro
# trabajo personal. No hemos sido ayudados por ninguna otra persona ni hemos obtenido la solución de fuentes externas,
# y tampoco hemos compartido nuestra solución con nadie. Declaramos además que no hemos realizado de manera deshonesta
# ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.

import sys
from pysparkling import Context

# sys.argv debe contener el nombre de fichero a procesar
if len(sys.argv) < 2:
    print "No se ha especificado fichero!"
    exit(-1)

path = sys.argv[1]
for i in range(2, len(sys.argv)):
    path += ","+sys.argv[i]

# 2.- Implementar una tarea Apache Spark que resuelva este problema utilizando transformaciones y acciones sobre RDDs.

# Creamos un contexto local y cargamos el fichero        
sc = Context()
lines = sc.textFile(path)

lista = (
  lines.map(lambda x: x.split('\t')) # Separamos por tabuladores
       .filter(lambda x: float(x[2]) < 2.0 and x[4] != '--') # Filtramos las palabras que nos interesan
       .top(5, lambda x: x[2]) # Obtenemos el top 5
)

# En lugar de almacenar en disco, recolectamos y mostramos por pantalla
for entry in lista:
   print entry[0], entry[2]

#sc.stop()
