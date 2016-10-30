# coding=utf-8

# Este fichero generado para la asignatura SGDI
# Practica 1 MapReduce Y Spark
# Autores: Antonio Calvo Morata y Carlos Congosto Sandoval

# Antonio Calvo Morata y Carlos Congosto Sandoval declaramos que esta solución es fruto exclusivamente de nuestro
# trabajo personal. No hemos sido ayudados por ninguna otra persona ni hemos obtenido la solución de fuentes externas,
# y tampoco hemos compartido nuestra solución con nadie. Declaramos además que no hemos realizado de manera deshonesta
# ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.

import sys
from pysparkling import Context

# sys.argv debe contener el nombre de fichero a procesar
if len(sys.argv) != 2:
  print "Falta el fichero!"
  exit(-1)



# Creamos un contexto local y cargamos el fichero        
sc = Context()
lines = sc.textFile(sys.argv[1])

counts = (
  lines.map(lambda x: x.split('\t')) # Dividimos en palabras y aplanamos
       .filter(lambda x: float(x[2]) < 2.0 and x[4] != '--')#filtramos las palabras que nos interesa
       .sortBy(lambda x: x[2],False)#ordenamos por la media
)

# En lugar de almacenar en disco, recolectamos y mostramos por pantalla
output = counts.collect()

for o in output[:5]:
    print o[0], '\t', o[2]

#sc.stop()
