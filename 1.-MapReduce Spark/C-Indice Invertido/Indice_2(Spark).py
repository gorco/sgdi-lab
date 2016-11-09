# coding=utf-8

# Este fichero generado para la asignatura SGDI
# Practica 1 MapReduce Y Spark, Ejercicio C.2
# Autores: Antonio Calvo Morata y Carlos Congosto Sandoval

# Antonio Calvo Morata y Carlos Congosto Sandoval declaramos que esta solución es fruto exclusivamente de nuestro
# trabajo personal. No hemos sido ayudados por ninguna otra persona ni hemos obtenido la solución de fuentes externas,
# y tampoco hemos compartido nuestra solución con nadie. Declaramos además que no hemos realizado de manera deshonesta
# ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.

import sys, re, string
from pyspark import SparkContext
from collections import Counter
import os

def wordsArray(text):
    text = text.encode('utf-8').replace('\'', ' ')  # Eliminamos apostrofes
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)  # quitamos los signos de puntuación
    words = text.split()
    listWords = []
    for word in words:
        word = re.sub(r'(\W)*', '', word)  # Obtenemos las palabras sin caracteres extraños
        word = word.lower()
        listWords.append(word)

    return listWords;

def filtroNumApariciones(tuple):
    for entry in dict(tuple[1]):
        if tuple[1][entry] > 20: # Si en algún libro hay más de 20 apariciones de la palabra el resultado hay que mandarlo
            return True;

    return False

# sys.argv debe contener el nombre del directorio donde se encuentran los archivos a procesar
if len(sys.argv) < 2 or len(sys.argv) > 3 or sys.argv[1].endswith("/"):
    print "Debe pasar la ruta a un directorio (sin '/' al final)"
    exit(-1)

path = sys.argv[1]

if not os.path.isdir(path):
    print "El path especificado no es un directorio"
    exit(-1)

# Creamos un contexto local y cargamos el fichero
sc = SparkContext(master="local")

rdd = sc.wholeTextFiles(path)
datos = (
    #Devuelve una tupla por cada palabra (sin apostrofes) con la palabra y el nombre del fichero
    # lista[-1] -> devuelve el ultimo elemento
    rdd.flatMap(lambda x: map(lambda y: (y, x[0].split("/")[-1]), wordsArray(x[1])))
        .groupByKey()
        .map(lambda x: (str(x[0]), dict(Counter(map(str, x[1]))))) #Cuenta las apariciones de los libros
                                                                 # ["libro1.txt, "libro2.txt","libro1.txt"] =>
                                                                 # => {"libro1.txt: 2, "libro2.txt": 1}
        .filter(filtroNumApariciones)
)

output = datos.collect()
for entry in output:
   print entry[0], entry[1]

sc.stop()