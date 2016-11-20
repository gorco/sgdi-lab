# coding=utf-8

# Este fichero generado para la asignatura SGDI
# Practica 2 Mineria de datos y recuperacion de la información, Ejercicio 3
# Autores: Antonio Calvo Morata y Carlos Congosto Sandoval

# Antonio Calvo Morata y Carlos Congosto Sandoval declaramos que esta solución es fruto exclusivamente de nuestro
# trabajo personal. No hemos sido ayudados por ninguna otra persona ni hemos obtenido la solución de fuentes externas,
# y tampoco hemos compartido nuestra solución con nadie. Declaramos además que no hemos realizado de manera deshonesta
# ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.

import string, os, sys, math, collections
from operator import itemgetter

# Dada una linea de texto, devuelve una lista de palabras no vacias 
# convirtiendo a minusculas y eliminando signos de puntuacion por los extremos
# Ejemplo:
#   > extrae_palabras("Hi! What is your name? John.")
#   ['hi', 'what', 'is', 'your', 'name', 'john']
def extrae_palabras(linea):
  return filter(lambda x: len(x) > 0, 
    map(lambda x: x.lower().strip(string.punctuation), linea.split()))


class VectorialIndex(object):

    def __init__(self, directorio, stop=[]):
        self.filesList = []
        self.invertedIndex = dict()
        # for doc in os.listdir(directorio):
            # file = open(doc, 'r')
        for path, subdirs, files in os.walk(directorio):
            # Creamos el indice invertido
            for name in files:
                idDoc = len(self.filesList)
                self.filesList.append(os.path.join(path, name))
                file = open(os.path.join(path, name),'r')
                # Leemos todas las palabras del archivo
                for l in file:
                    line = extrae_palabras(l)
                    for word in line:
                        if word not in stop: # Si es una palabra no "censurada"
                            # Si no hay una entrada en el indice la creamos con el valor de una lista con la tupla
                            # de ese id y 1 (ha aparecido una vez)
                            if word not in self.invertedIndex:
                                self.invertedIndex[word] = [(idDoc, 1)]
                            # Si la palabra ya ha aparecido en el archivo le sumamos uno al contador de veces q aparece
                            else :
                                lastTuple = self.invertedIndex[word][-1]
                                if idDoc == lastTuple[0]:
                                    self.invertedIndex[word][-1] = (lastTuple[0], lastTuple[1]+1)
                                # Sino iniciamos la cuenta en uno
                                else :
                                    self.invertedIndex[word].append((idDoc, 1))

        # Sustituimos el número de apariciones por el valor TD-IDF de cada palabra en cada documento
        totalFiles = len(self.invertedIndex)
        self.norma = [0] * totalFiles;
        for key, values in self.invertedIndex.items():
            tuplelist = []
            for tuple in values:
                # TF-IDF(i,j) = TF(i,j) * IDF(i,j) = (1+log(f(i,j))) * log(N/n(i)
                tdidf = (1 + math.log(tuple[1], 2)) * math.log(totalFiles/len(values), 2)
                tuplelist.append((tuple[0], tdidf))
                self.norma[tuple[0]] += math.pow(tdidf, 2)
            self.invertedIndex[key] = tuplelist

        i = 0
        for value in self.norma:
            self.norma[i] = math.sqrt(value)
            i+=1;


    ###########################################
    #                                         #
    #     CONSULTA VECTORIAL                  #
    #                                         #
    ###########################################
    def consulta_vectorial(self, consulta, n=3):
        scores = [(0, 0)] * len(self.filesList) # Inicializamos el producto escalar parcial asociado a cada documento d (en total hay N)
        # Obtenemos la lista [(doc,peso),...(doc,peso)] asociada al término t
        words = consulta.split()
        for word in words:
            p = self.invertedIndex[word] # Pesos del término word en cada documento
            # Sumamos el peso en cada producto escalar parcial
            for (id, peso) in p:
                scores[id] = (id, scores[id][1]+peso)  # No hay producto
        # Dividimos entre la norma | d |
        for id in range(len(self.filesList)):
            scores[id] = (id, scores[id][1]/self.norma[id])
        # Obtenemos los k documentos con mayor relevancia
        scores.sort(key=itemgetter(1), reverse=True)

        # Trasformamos los ids al nombre de los ficheros
        result = []
        for tuple in scores[0:n] :
            result.append((self.filesList[tuple[0]], tuple[1]))

        return result


    ###########################################
    #                                         #
    #     CONSULTA CONJUNCION                 #
    #                                         #
    ###########################################
    def consulta_conjuncion(self, consulta):
        words = consulta.split()
        result = []
        if len(words) > 1 :
            appearances = []
            # Obtenemos la lista de ids de archivos donde aparece cada palabra de la consulta
            for word in words:
                appearances.append(self.invertedIndex[word])

            # Algoritmo de intersección de un conjunto de listas
            terms = sorted(appearances, key=len)
            answer = terms[0]
            terms = terms[1:]
            while terms != None and answer != None:
                e = terms[0]
                answer = self.intersect(answer, e)
                if len(terms) > 1:
                    terms = terms[1:]
                else :
                    terms = None

            # Trasformamos los ids al nombre de los ficheros
            for tuple in answer:
                result.append(self.filesList[tuple[0]])
        else :
            # Si la consulta sólo tiene una palabra devolvemos directamente los archivos donde aparece
            for tuple in self.invertedIndex[words[0]] :
                result.append(self.filesList[tuple[0]])

        return result

    # Función para la intersección de dos listas
    def intersect(self,list1, list2):
        answer = []
        it1 = iter(list1)
        it2 = iter(list2)
        p1 = it1.next()
        p2 = it2.next()
        while True:
            try:
                if p1[0] == p2[0]:
                    answer.append(p1)
                    p1 = it1.next()
                    p2 = it2.next()
                elif p1[0] < p2[0]:
                    p1 = it1.next()
                else:
                    p2 = it2.next()
            except StopIteration:
                break
        return answer


# Como argumentos recibe:
# argv[1] = Directorio de la coleccion  (OBLIGATORIO)
# argv[2:n] = Palabras para la consulta (OPCIONAL)
#      * Si arg[2] es un numero se usará como cantidad de documentos a mostrar en la consulta vectorial
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "No se ha especificado directorio!"
        exit(-1)

    root = sys.argv[1]

    request = ""
    n = 2
    if(len(sys.argv) > 2) :
        k = 2
        if(sys.argv[2].isdigit()):
            n = int(sys.argv[2])
            k += 1
        request = sys.argv[k]
        for i in range(k+1, len(sys.argv)):
            request += " "+str(sys.argv[i])
    # Valor de consulta por defecto si no se pasan como argumento
    else  :
        request = "civil war"

    v = VectorialIndex(root,[])
    print(v.consulta_conjuncion(request))
    print(v.consulta_vectorial(request, n))
