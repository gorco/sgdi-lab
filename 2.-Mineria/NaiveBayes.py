# coding=utf-8

# Este fichero generado para la asignatura SGDI
# Practica 2, Ejercicio 1. Naive Bayes
# Autores: Antonio Calvo Morata y Carlos Congosto Sandoval

# Antonio Calvo Morata y Carlos Congosto Sandoval declaramos que esta solución es fruto exclusivamente de nuestro
# trabajo personal. No hemos sido ayudados por ninguna otra persona ni hemos obtenido la solución de fuentes externas,
# y tampoco hemos compartido nuestra solución con nadie. Declaramos además que no hemos realizado de manera deshonesta
# ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.


import csv,math,ast


class NaiveBayes(object):
    probabilidades = []
    classesAux =[]

    def __init__(self, fichero, smooth=1):
        file = open(fichero,'r')
        #next(file, None) #ignoramos la línea de cabecera
        #fieldNames=['day','season','wind','rain','class']
        reader = csv.DictReader(file)

        fieldNames = reader.fieldnames
        listaMain = []#Lista que tendrá las listas de atributos


        # Creamos tantas listas como columnas hay en el fichero
        for i in range(len(fieldNames)):
            listAux = []
            listaMain.append(listAux)


        tuplas = [] #lista con la tupla de cada pareja de atributo clase

        #leemos y guardamos los datos del fichero
        for row in reader:
            for i in range(len(row)):
                listaMain[i].append(row[fieldNames[i]])
                tupla = (row[fieldNames[i]],row['class'])
                tuplas.append(tupla)

        print '\nTotal instancias: ',reader.line_num-1 #imprimimos el numero de instancias leidas del fichero

        #Mostramos los posibles valores para cada atributo
        print '\n'
        self.classesAux = list(set(listaMain[len(listaMain)-1]))
        contador= 0
        for name in fieldNames:
            print 'Atributo ',name, ': ', set(listaMain[contador])
            contador+=1

        #Mostramos el número de veces que aparece cada clase
        print '\n'
        for clase in self.classesAux:
            print 'Intancias clase ',clase,': ',listaMain[len(listaMain)-1].count(clase)

        # imprimir las instancias con los posibles valores
        print '\n'
        for c in self.classesAux:
            for cont in range(len(listaMain)-1):
                for atributo in list(set(listaMain[cont])):
                    tuplaFind=(atributo,c)
                    cuantas = tuplas.count(tuplaFind)
                    print 'Instancias (',fieldNames[cont],' = ', atributo, ', class = ', c, '): ', cuantas
                    if smooth:
                        if cuantas == 0: prob = 0
                        else:
                            prob = 1+math.log(cuantas,2)
                    else: prob=cuantas/len(tuplas)

                    dicc = dict(nombre=atributo, clase=c, prob = prob)
                    self.probabilidades.append(dicc)

        file.close()




    def clasifica(self, instancia):
        prob = 0
        probCan = 0
        candidata = ''
        print '\n'
        for clase in self.classesAux:
            for key in instancia.keys():
                for dic in self.probabilidades:
                    if dic.get('nombre') == instancia.get(key) and dic.get('clase')==clase:
                        prob += dic.get('prob')
                        #print 'atributo: ',instancia.get(key),' clase: ',clase,'::>', dic.get('prob')
            if prob > probCan: candidata = clase

        print 'Clase predicha: ',candidata
        return candidata


    def test(self, fichero):
        aciertos = 0
        fallos = 0

        return (aciertos, fallos, aciertos/(aciertos+fallos))


