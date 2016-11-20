# coding=utf-8

# Este fichero generado para la asignatura SGDI
# Practica 2, Ejercicio 1. Naive Bayes
# Autores: Antonio Calvo Morata y Carlos Congosto Sandoval

# Antonio Calvo Morata y Carlos Congosto Sandoval declaramos que esta solución es fruto exclusivamente de nuestro
# trabajo personal. No hemos sido ayudados por ninguna otra persona ni hemos obtenido la solución de fuentes externas,
# y tampoco hemos compartido nuestra solución con nadie. Declaramos además que no hemos realizado de manera deshonesta
# ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.


import csv


class NaiveBayes(object):
    probabilidades = [] #lista con las probabilidades de cada opción
    classesAux =[] #lista que contendrá los posibles valores de clase
    listaMain = []  # Lista que tendrá las listas de atributos
    tamMain = 0 #longitud de la lista de listas
    intstancias = 0 #número de instancias leídas

    def __init__(self, fichero, smooth=1):
        file = open(fichero,'r')
        reader = csv.DictReader(file)
        fieldNames = reader.fieldnames #creamos una lista con los nombres de los atributos

        # Creamos tantas listas como columnas hay en el fichero
        for i in range(len(fieldNames)):
            listAux = []
            self.listaMain.append(listAux)


        tuplas = [] #lista con la tupla de cada pareja de atributo clase
        self.tamMain = len(self.listaMain) #actualizamos el valor del tamaño de la lista principal

        #leemos y guardamos los datos del fichero
        for row in reader:
            for i in range(len(row)):
                self.listaMain[i].append(row[fieldNames[i]])
                tupla = (row[fieldNames[i]],row['class'])
                tuplas.append(tupla)

        self.intstancias = reader.line_num-1 #actuliazamos las instancias leídas
        print '\nTotal instancias: ',self.intstancias #imprimimos el numero de instancias leidas del fichero

        #Mostramos los posibles valores para cada atributo
        print '\n'
        self.classesAux = list(set(self.listaMain[self.tamMain-1]))
        contador= 0
        for name in fieldNames:
            print 'Atributo ',name, ': ', set(self.listaMain[contador])
            contador+=1

        #Mostramos el número de veces que aparece cada clase
        print '\n'
        for clase in self.classesAux:
            print 'Intancias clase ',clase,': ',self.listaMain[self.tamMain-1].count(clase)

        # imprimir las instancias con los posibles valores
        print '\n'
        for c in self.classesAux:
            for cont in range(self.tamMain-1):
                for atributo in list(set(self.listaMain[cont])):
                    tuplaFind=(atributo,c)
                    cuantas = tuplas.count(tuplaFind)
                    print 'Instancias (',fieldNames[cont],' = ', atributo, ', class = ', c, '): ', cuantas

                    if smooth: #El suavizado de Lapace está activado
                        prob = (1.0 + cuantas)/self.listaMain[self.tamMain-1].count(c)
                    else:
                        prob=float(cuantas)/self.listaMain[self.tamMain-1].count(c)

                    dicc = dict(nombre=atributo, clase=c, prob = prob) #creamos un diccionario con la información
                                                                        # de la tupla y la probabilidad de cada una
                    self.probabilidades.append(dicc)#almacenamos el diccionario en la lista

        if smooth == 0:
            for c in self.classesAux:
                dicc = dict(nombre = '---',clase=c,prob=self.listaMain[self.tamMain-1].count(c)/float(self.intstancias))
                self.probabilidades.append(dicc)
        file.close()#Cerramos el fichero


    def clasifica(self, instancia):
        probCan = 0 #Probabilidad de la clase candidata
        candidata = '' #Clase candidata
        prob = 0

        #Recorremos cada posible clase y calculamos su probabilidad
        for clase in self.classesAux:
           # prob = self.listaMain[self.tamMain - 1].count(clase) / float(self.intstancias)
            for key in instancia.keys():
                for dic in self.probabilidades:
                    if dic.get('nombre') == instancia.get(key) and dic.get('clase')==clase:
                        prob += dic.get('prob')

            if prob > probCan: #Miramos si la probabilidad actual es mayor que la candidata
                probCan = prob
                candidata = clase

        print '\n'
        print 'Clase predicha: ',candidata
        return candidata


    def test(self, fichero):
        aciertos = 0
        fallos = 0

        return (aciertos, fallos, aciertos/(aciertos+fallos))


