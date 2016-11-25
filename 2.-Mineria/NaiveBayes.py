# coding=utf-8

# Este fichero generado para la asignatura SGDI
# Practica 2, Ejercicio 1. Naive Bayes
# Autores: Antonio Calvo Morata y Carlos Congosto Sandoval

# Antonio Calvo Morata y Carlos Congosto Sandoval declaramos que esta solución es fruto exclusivamente de nuestro
# trabajo personal. No hemos sido ayudados por ninguna otra persona ni hemos obtenido la solución de fuentes externas,
# y tampoco hemos compartido nuestra solución con nadie. Declaramos además que no hemos realizado de manera deshonesta
# ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.


import csv,math


class NaiveBayes(object):
    probabilidades = [] #lista con las probabilidades de cada opción
    listaMain = []  # Lista que tendrá las listas de atributos
    clases = []

    def __init__(self, fichero, smooth=1):
        file = open(fichero,'r')
        reader = csv.DictReader(file)
        fieldNames = reader.fieldnames #creamos una lista con los nombres de los atributos
        parejas = []
        listaClases = []


        for row in reader:
            self.listaMain.append(row)
            clase = row['class']
            listaClases.append((clase))
            for i in range(len(fieldNames)-1):
                parejas.append({fieldNames[i]:row[fieldNames[i]],'class':clase})

        print 'Instancias leidas: ', len(self.listaMain),'\n'

        #Creamos tantos conjuntos como atributos hay
        conjuntos = []
        for lista in range(len(reader.fieldnames)):
            conjuntos.append(set())

        for instancia in self.listaMain:
            cont = 0
            for it in range(len(fieldNames)):
                conjuntos[cont].add((instancia.get(fieldNames[cont])))
                cont+=1


        for c in range(len(fieldNames)-1):
            print 'Atributo ', fieldNames[c],': ',list(conjuntos[c])

        self.clases = list(conjuntos[len(fieldNames)-1])
        print 'Clase: ', self.clases,'\n'

        for clase in self.clases:
            print 'Instancias clase ', clase, ': ', listaClases.count(clase)
        print '\n'

        for c in self.clases:
            for cont in range(len(fieldNames)-1):
                for atributo in conjuntos[cont]:
                    cuantas = parejas.count({fieldNames[cont]:row[fieldNames[cont]],'class':c})
                    print 'Instancias (', fieldNames[cont], ' = ', atributo, ', class = ', c, '): ', cuantas

                    prob = float(smooth + cuantas) / (listaClases.count(c)+(len(conjuntos[cont])*smooth))

                    dicc = dict(nombre=atributo, clase=c, prob=prob)  # creamos un diccionario con la información
                                                                    # de la tupla y la probabilidad de cada una
                    self.probabilidades.append(dicc)  # almacenamos el diccionario en la lista
        print '\n'

        file.close()


    def clasifica(self, instancia):
        probCan = 0 #Probabilidad de la clase candidata
        candidata = '' #Clase candidata


        #Recorremos cada posible clase y calculamos su probabilidad
        for clase in self.clases:
            prob = 0
            for key in instancia.keys():
                for dic in self.probabilidades:
                    if dic.get('nombre') == instancia.get(key) and dic.get('clase')==clase:
                        if dic.get('prob')==0.0:
                            prob -= 0
                        else:
                            prob -= math.log(dic.get('prob'),2)
            #print 'Clase: ',clase, ' Prob: ',prob
            if prob > probCan: #Miramos si la probabilidad actual es mayor que la candidata
                probCan = prob
                candidata = clase

        return candidata


    def test(self, fichero):
        aciertos = 0
        fallos = 0
        lista = []

        file = open(fichero, 'r')
        reader = csv.DictReader(file)

        print 'TEST'
        for row in reader:
            clase = row['class']
            del row['class']
            print row, '-',clase
            predicha = self.clasifica(row)
            print 'Clase predicha: ', predicha
            if predicha == clase:
                print '\t--> Acierto'
                aciertos+=1

            else:
                print '\t--> Fallo'
                fallos+=1

        return (aciertos, fallos, aciertos/float(aciertos+fallos))


