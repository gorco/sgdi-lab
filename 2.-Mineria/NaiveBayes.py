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

    def __init__(self, fichero, smooth=1):
        file = open(fichero,'r')
        next(file, None) #ignoramos la línea de cabecera la línea de cabe
        reader = csv.reader(file)
        count = 0
        days = set()
        seasons =set()
        winds= set()
        rains=set()
        clases=set()
        for row in reader:
            count+=1
            days.add(row[0])
            seasons.add(row[1])
            winds.add(row[2])
            rains.add(row[3])
            clases.add(row[4])

        print days
        print seasons
        print winds
        print rains
        print clases


        print 'Total instancias: ',count
        atributos = []
        for atributo in atributos: #imprime los posibles valores para cada atributo
            pass
        clases =  []
        for clase in clases:
            pass

        #imprimir las instancias con los posibles valores
        file.close()


    def clasifica(self, instancia):
        pass        

    def test(self, fichero):
        pass


if __name__ == '__main__':
    nb = NaiveBayes('train.data',1)