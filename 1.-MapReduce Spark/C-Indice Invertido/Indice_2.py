# coding=utf-8

# Este fichero generado para la asignatura SGDI
# Practica 1 MapReduce Y Spark
# Autores: Antonio Calvo Morata y Carlos Congosto Sandoval

# Antonio Calvo Morata y Carlos Congosto Sandoval declaramos que esta solución es fruto exclusivamente de nuestro
# trabajo personal. No hemos sido ayudados por ninguna otra persona ni hemos obtenido la solución de fuentes externas,
# y tampoco hemos compartido nuestra solución con nadie. Declaramos además que no hemos realizado de manera deshonesta
# ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.

import sys, re, string
from pysparkling import Context
# sys.argv debe contener el nombre de fichero a procesar
if len(sys.argv) != 4:
    print "Falta algún fichero!"
    exit(-1)

# Creamos un contexto local y cargamos el fichero
sc = Context()

def function(x):
    return x[0].encode('utf-8'), (sys.argv[file], x[1])

#función que modifica las palabras a minúsculas quitando signos de puntuación
# return pareja (palabra, 1)
def iguala(x):
    x = x.lower() #Ponemos todo con minúsculas
    x = re.sub('[%s]' % re.escape(string.punctuation), '', x)#quitamos los signos de puntuación
    return x,1 #devolvemos la tupla


for file in range(1,4):#se recorren todas los argumentos de la llamada
    lines = sc.textFile(sys.argv[file])

    datos = (
        lines.flatMap((lambda x: x.split(' ')))  # Dividimos en palabras y aplanamos
            .map(iguala)    #creamos la pareja palabra,1
            .reduceByKey(lambda x,y: x+y) #sumamos el número de apariciones
            .filter(lambda x: x[1] > 20 and x[0] != '') #quitamos las palabras que se repiten menos de 20 veces
            .map(function) #creamos la tupla  (palabra, (libro, apariciones))
    )

    output = datos.collect()
    print output