# coding=utf-8

# Este fichero generado para la asignatura SGDI
# Practica 2 Mineria de datos y recuperacion de la información, Ejercicio 3
# Autores: Antonio Calvo Morata y Carlos Congosto Sandoval

# Antonio Calvo Morata y Carlos Congosto Sandoval declaramos que esta solución es fruto exclusivamente de nuestro
# trabajo personal. No hemos sido ayudados por ninguna otra persona ni hemos obtenido la solución de fuentes externas,
# y tampoco hemos compartido nuestra solución con nadie. Declaramos además que no hemos realizado de manera deshonesta
# ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.

import string, os, sys, math, collections

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
        for path, subdirs, files in os.walk(root):
            # Creamos el indice invertido
            for name in files:
                idDoc = len(self.filesList)
                self.filesList.append(name)
                file = open(os.path.join(path, name),'r')
                # Leemos todas las palabras del archivo
                for l in file:
                    line = extrae_palabras(l)
                    for word in line:
                        if word not in stop: # Si es una palabra no "censurada"
                            # Si no hay una entrada en el indice la creamos con el valor de un diccionario ordenado vacio
                            if not word in self.invertedIndex:
                                self.invertedIndex[word] = collections.OrderedDict()
                            # Si la palabra ya ha aparecido en el archivo le sumamos uno al contador de veces q aparece
                            if idDoc in self.invertedIndex[word]:
                                self.invertedIndex[word][idDoc] += 1
                            # Sino iniciamos la cuenta en uno
                            else :
                                self.invertedIndex[word][idDoc] = 1

        # Sustituimos el número de apariciones por el valor TD-IDF de cada palabra en cada documento
        totalFiles = len(self.invertedIndex)
        for key, values in self.invertedIndex.items():
            tuplelist = []
            for id, count in values.items():
                # TF-IDF(i,j) = TF(i,j) * IDF(i,j) = (1+log(f(i,j))) * log(N/n(i)
                tuplelist.append((id, (1 + math.log(count, 2)) * math.log(totalFiles/len(values), 2)))
            self.invertedIndex[key] = tuplelist

    def consulta_vectorial(self, consulta, n=3):
        pass

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

            for id in answer:
                result.append(self.filesList[id])
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
                    answer.append(p1[0])
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
# arg[1] = Directorio de la coleccion  (OBLIGATORIO)
# arg[2:n] = Palabras para la consulta (OPCIONAL)
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "No se ha especificado directorio!"
        exit(-1)

    root = sys.argv[1]

    request = ""
    if(len(sys.argv) > 2) :
        request = sys.argv[2]
        for i in range(3, len(sys.argv)):
            request += " "+str(sys.argv[i])
    # Valor de consulta por defecto si no se pasan como argumento
    else  :
        request = "civil war"

    v = VectorialIndex(root,[])
    print(v.consulta_conjuncion(request))
