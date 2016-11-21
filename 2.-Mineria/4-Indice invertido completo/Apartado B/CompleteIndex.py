# coding=utf-8

# Este fichero generado para la asignatura SGDI
# Practica 2 Mineria de datos y recuperacion de la información, Ejercicio 4.B
# Autores: Antonio Calvo Morata y Carlos Congosto Sandoval

# Antonio Calvo Morata y Carlos Congosto Sandoval declaramos que esta solución es fruto exclusivamente de nuestro
# trabajo personal. No hemos sido ayudados por ninguna otra persona ni hemos obtenido la solución de fuentes externas,
# y tampoco hemos compartido nuestra solución con nadie. Declaramos además que no hemos realizado de manera deshonesta
# ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.

import string, os, sys, math
from bitarray import bitarray

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
        self.compress = compresion
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
                listDif = []
                #**********************#
                #   COMPRESION NONE    #
                #**********************#
                if compresion == None:
                    listDif = [tuple[1][0]]
                    for pos in range (1, numAppears):
                        listDif.append(tuple[1][pos]-tuple[1][pos-1])
                # **********************#
                #   COMPRESION UNARIA   #
                # **********************#
                elif compresion == 'unary':
                    listDif = ''
                    for i in range(tuple[1][0]-1):
                        listDif += '1'
                    listDif+='0'
                    for pos in range (1, numAppears):
                        for k in range((tuple[1][pos]-tuple[1][pos-1]-1)):
                            listDif += '1'
                        listDif += '0'
                    listDif = bitarray(listDif)
                # ********************************#
                #   COMPRESION BYTES VARIABLES    #
                # ********************************#
                elif compresion == 'variable-bytes':
                    listDif = self.toBytes(tuple[1][0])
                    for pos in range(1, numAppears):
                        listDif += self.toBytes(tuple[1][pos] - tuple[1][pos - 1])
                    listDif = bitarray(listDif)
                # ****************************#
                #   COMPRESION ELIAS-GAMMA    #
                # ****************************#
                elif compresion == 'elias-gamma':
                    listDif = self.toEliasGamma(tuple[1][0])
                    for pos in range (1, numAppears):
                        listDif += self.toEliasGamma(tuple[1][pos]-tuple[1][pos-1])
                # ****************************#
                #   COMPRESION ELIAS-DELTA    #
                # ****************************#
                elif compresion == 'elias-delta':
                    listDif = self.toEliasDelta(tuple[1][0])
                    for pos in range(1, numAppears):
                        listDif += self.toEliasDelta(tuple[1][pos] - tuple[1][pos - 1])

                tuplelist.append((tuple[0], tdidf, listDif)) #(id, peso, diferencia posiciones)
                self.norma[tuple[0]] += math.pow(tdidf, 2)
            self.invertedIndex[key] = tuplelist

        i = 0
        for value in self.norma:
            self.norma[i] = math.sqrt(value)
            i += 1;

    ###########################################
    #     Funcion auxiliar toEliasGamma       #
    ###########################################
    # Dado un número devuelve su representacion en elias-gamma
    def toEliasGamma(self, val):
        if val == 1 :
            return '0'

        binario = str(bin(val))[2:]  # Quitamos el '0b' de haber convertido a binario
        offset = str(binario[1:])
        longitud = len(binario)
        lUnario = ''
        for z in range(longitud-1):
            lUnario += '1'
        lUnario += '0'
        return lUnario + str(offset)

    ###########################################
    #     Funcion auxiliar toEliasDelta       #
    ###########################################
    # Dado un número devuelve su representacion en elias-gamma
    def toEliasDelta(self, val):
        if val == 1:
            return '0'

        binario = str(bin(val))[2:]  # Quitamos el '0b' de haber convertido a binario
        offset = str(binario[1:])
        longitud = len(binario)
        lBinario = self.toEliasGamma(longitud)
        return lBinario + str(offset)

    ###########################################
    #     Funcion auxiliar toBytes            #
    ###########################################
    # Dado un número devuelve su representacion en elias-gamma
    def toBytes(self, val):
        value = ''
        num = str(bin(val))[2:]
        bytes = (int(len(num))-1) / 7
        fill = (int(len(num))+1*bytes) % 8
        for i in range(bytes+1):
            if i == bytes:
                value += '1'
            else :
                value += '0'

            if i == 0:
                for j in range(7-fill):
                    value += '0'
                for k in range(fill):
                    value += num[k]
                num = num[fill:]
            else :
                value += num[:7]
                num = num[7:]
        return value

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
    #     Funcion auxiliar decompress         #
    ###########################################
    # Dada un bitarray devuelve su traducción a lista de diferencias
    def decompress(self, bitArray) :
        list = []
        # **********************#
        #   DESCOMPRESION NONE    #
        # **********************#
        if self.compress == None:
            return bitArray
        # **********************#
        #   DESCOMPRESION UNARIA   #
        # **********************#
        elif self.compress == 'unary':
            num = 0
            for bit in bitArray:
                if bit == 0:
                    list.append(num + 1)
                    num = 0
                else:
                    num += 1
        # ********************************#
        #   DESCOMPRESION BYTES VARIABLES    #
        # ********************************#
        elif self.compress == 'variable-bytes' :
            number = ''
            flush = False
            for i in range(len(bitArray)):
                bit = str(int(bitArray[i]))
                if i % 8 != 0:
                    number += bit
                else :
                    if flush:
                        list.append(int(str(number), 2))
                        number = ''
                        flush = False
                    if bit == '1':
                        flush = True
            if flush:
                list.append(int(str(number), 2))

        # ****************************#
        #   DESCOMPRESION ELIAS-GAMMA #
        # ****************************#
        elif self.compress == 'elias-gamma' or self.compress == 'elias-delta':
            noEnd = True
            while noEnd:
                lUnario = 0
                num = 0
                offset = ''
                for bit in bitArray:
                    if int(bit) == 0:
                        lUnario = num + 1
                        break
                    else:
                        num += 1
                bitArray = bitArray[lUnario:]
                for i in range(lUnario-1):
                    offset += str(int(bitArray[i]))
                if len(bitArray) == lUnario-1 :
                    noEnd = False
                else :
                    bitArray = bitArray[lUnario-1:]
                binario = '1'+offset
                eliasGamma = int(str(binario), 2)
                # ******************************#
                #   DESCOMPRESION ELIAS-DELTA   #
                # ******************************#
                if self.compress == 'elias-delta': # Si es elias Delta sacamos el offset a partir del número EliasGamma
                    offset = ''
                    for j in range(eliasGamma - 1):
                        offset += str(int(bitArray[j]))
                    binario = '1' + offset
                    eliasDelta = int(str(binario), 2)
                    list.append(eliasDelta)
                    if len(bitArray) == eliasGamma - 1:
                        noEnd = False
                    else:
                        bitArray = bitArray[eliasGamma - 1:]
                else :
                    list.append(eliasGamma)

        return list

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
            list1 = self.decompress(listList[0][2])
            listList = listList[1:]

            list2 = self.decompress(listList[0][2])
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
                    list2 = self.decompress(listList[0][2])
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
        size = 0
        for values in self.invertedIndex.values():
            for tuple in values:
                if self.compress == None:
                    numAppears = len(tuple[2])
                    size += 32*numAppears
                else :
                    size += len(tuple[2])
        return size

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

    #v = CompleteIndex(root)
    #v = CompleteIndex(root, 'unary')
    #v = CompleteIndex(root, 'variable-bytes')
    #v = CompleteIndex(root, 'elias-gamma')
    v = CompleteIndex(root, 'elias-delta')

    #print(v.consulta_frase(request))
    print(v.compress, v.num_bits())

