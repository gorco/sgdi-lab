# coding=utf-8

# Este fichero generado para la asignatura SGDI
# Practica 2 Mineria de datos y recuperacion de la información, Ejercicio 4.A
# Autores: Antonio Calvo Morata y Carlos Congosto Sandoval

# Antonio Calvo Morata y Carlos Congosto Sandoval declaramos que esta solución es fruto exclusivamente de nuestro
# trabajo personal. No hemos sido ayudados por ninguna otra persona ni hemos obtenido la solución de fuentes externas,
# y tampoco hemos compartido nuestra solución con nadie. Declaramos además que no hemos realizado de manera deshonesta
# ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.

import string, os, sys, math

# Dada una linea de texto, devuelve una lista de palabras no vacias 
# convirtiendo a minusculas y eliminando signos de puntuacion por los extremos
# Ejemplo:
#   > extrae_palabras("Hi! What is your name? John.")
#   ['hi', 'what', 'is', 'your', 'name', 'john']
def extrae_palabras(linea):
  return filter(lambda x: len(x) > 0, 
    map(lambda x: x.lower().strip(string.punctuation), linea.split()))


class CompleteIndex(object):

    def __init__(self, directorio, compresion=None):
        self.filesList = []
        self.invertedIndex = dict()
        # for doc in os.listdir(directorio):
        # file = open(doc, 'r')
        for path, subdirs, files in os.walk(directorio):
            # Creamos el indice invertido
            for name in files:
                idDoc = len(self.filesList)
                posWord = 1 # Posicion de palabra en el documento
                self.filesList.append(os.path.join(path, name))
                file = open(os.path.join(path, name), 'r')
                # Leemos todas las palabras del archivo
                for l in file:
                    line = extrae_palabras(l)
                    for word in line:
                        # Si no hay una entrada en el indice la creamos con el valor de una lista con la tupla
                        # de ese id y posicion de palabra que aparece en el documento
                        if word not in self.invertedIndex:
                            self.invertedIndex[word] = [(idDoc, [posWord])]
                        # Si la palabra ya ha aparecido en el archivo le concatenamos la posicion de palabra si el
                        # documento existe y sino creamos una nueva tupla
                        else:
                            lastTuple = self.invertedIndex[word][-1]
                            if idDoc == lastTuple[0]:
                                lastTuple[1].append(posWord)
                                self.invertedIndex[word][-1] = (lastTuple[0], lastTuple[1])
                            # Sino insertamos una nueva tupla con el nuevo doc y la posicion de la palabra
                            else:
                                self.invertedIndex[word].append((idDoc, [posWord]))

                        posWord+=1

        # Añadimos el peso TD-IDF de cada palabra en cada documento
        # Además comprimimos las listas de posiciones por listas de diferencias
        totalFiles = len(self.invertedIndex)
        self.norma = [0] * totalFiles;
        for key, values in self.invertedIndex.items():
            tuplelist = []
            for tuple in values:
                numAppears = len(tuple[1])
                # TF-IDF(i,j) = TF(i,j) * IDF(i,j) = (1+log(f(i,j))) * log(N/n(i)
                tdidf = (1 + math.log(numAppears, 2)) * math.log(totalFiles / len(values), 2)
                # Comprimimos la lista de apariciones
                listDif = [tuple[1][0]]
                for pos in range (1, numAppears):
                    listDif.append(tuple[1][pos]-tuple[1][pos-1])
                tuplelist.append((tuple[0], tdidf, listDif)) #(id, peso, diferencia posiciones)
                self.norma[tuple[0]] += math.pow(tdidf, 2)
            self.invertedIndex[key] = tuplelist

        i = 0
        for value in self.norma:
            self.norma[i] = math.sqrt(value)
            i += 1;


    ###########################################
    #                                         #
    #     CONSULTA FRASE                      #
    #                                         #
    ###########################################
    def consulta_frase(self, frase):
        words = frase.split()
        result = []
        appearances = []
        if len(words) > 0:
            # Obtenemos la lista de ids de archivos donde aparece cada palabra de la consulta
            for word in words:
                appearances.append(self.invertedIndex[word])

        cont = True
        answer = []
        while cont:
            if self.sameDocID(appearances):
                if self.consecutive(appearances):
                    answer.append(appearances[0][0][0]) #Añadimos a los resultados el id del archivo actual
                appearances = self.advanceAll(appearances)
            else:
                appearances = self.advanceMin(appearances)
            cont = self.allNoNone(appearances)

        result = []
        for id in answer:
            result.append(self.filesList[id])

        return result

    ###########################################
    #     Funcion auxiliar sameDocID          #
    ###########################################
    # Dada una lista de listas de tuplas con el id del documento, el peso y una lista de apariciones comprueba si todas
    # las cabezas de lista (la primera tupla) pertenecen al mismo documento
    def sameDocID(self, listOflist) :
        id = listOflist[0][0][0]
        for list in listOflist :
            if id != list[0][0] :
                return False
        return True

    ###########################################
    #     Funcion auxiliar advanceAll         #
    ###########################################
    # Dada una lista de listas de tuplas con el id del documento, el peso y una lista de apariciones desvuelve
    # la lista de todas las colas (quita las cabezas de lista)
    def advanceAll(self, listOfList):
        newList = []
        for list in listOfList :
            if len(list) > 1:
                newList.append(list[1:])
            else :
                newList.append(None)
        return newList

    ###########################################
    #     Funcion auxiliar advanceMin         #
    ###########################################
    # Dada una lista de listas de tuplas con el id del documento, el peso y una lista de apariciones quita las cabezas
    # de lista de todas aquellas listas que no tengan el id de documento maximo
    def advanceMin(self, listOfList):
        max = 0
        for list in listOfList:
            if list[0][0] > max:
                max = list[0][0]

        newList = []
        for list in listOfList:
            if list[0][0] < max :
                if len(list) > 1:
                    newList.append(list[1:])
                else :
                    newList.append(None)
            else :
                newList.append(list)
        return newList

    ###########################################
    #     Funcion auxiliar allNoNone         #
    ###########################################
    # Comprueba que no haya un valor None en una lista de listas de tuplas con el id del documento, el peso y una lista
    # de apariciones
    def allNoNone(self, listOfList) :
        for list in listOfList :
            if list == None :
                return False
        return True

    ###########################################
    #     Funcion auxiliar consecutive         #
    ###########################################
    # Dada una lista de listas de tuplas con el id del documento, el peso y una lista de apariciones
    # Comprueba que la primera tupla de todas las listas (y que son del mismo documento) sean consecutivas
    # lo que quiere decir que la frase está en el documento
    def consecutive(self, listOfList) :
        listList = []
        for list in listOfList:
            listList.append(list[0])
        pos = 0

        if len(listList) > 1:
            list1 = listList[0][2]
            listList = listList[1:]

            list2 = listList[0][2]
            listList = listList[1:]

            noEnd = True
            newList = []
            while noEnd :
                noFinish = True
                while noFinish:
                    if int(list1[0]) == int(list2[0])-1 : #son consecutivos
                        newList.append(list2[0])
                        if len(list1) > 1 and len(list2) > 1:
                            oldPos = list1[0]
                            list1 = list1[1:]
                            list1[0] += oldPos
                            oldPos = list2[0]
                            list2 = list2[1:]
                            list2[0] += oldPos
                        else :
                            noFinish = False
                    elif list1[0] < list2[0]:
                        if len(list1) > 1 :
                            oldPos = list1[0]
                            list1 = list1[1:]
                            list1[0] += oldPos
                        else :
                            noFinish = False
                    else :
                        if len(list2) > 1:
                            oldPos = list2[0]
                            list2 = list2[1:]
                            list2[0] += oldPos
                        else :
                            noFinish = False

                if len(newList) != 0 and len(listList) > 1:
                    list1 = newList
                    newList = []
                    listList = listList[1:]
                    list2 = listList[0][2]
                else :
                    noEnd = False

            return len(newList) != 0

        return True

    ###########################################
    #                                         #
    #     CALCULA NUMERO DE BITS              #
    #                                         #
    ###########################################
    def num_bits(self):
        pass

# Como argumentos recibe:
# argv[1] = Directorio de la coleccion  (OBLIGATORIO)
# argv[2:n] = Palabras para la consulta (OPCIONAL)
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

    v = CompleteIndex(root,[])
    print(v.consulta_frase(request))