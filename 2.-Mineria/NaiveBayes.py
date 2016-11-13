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
        next(file, None) #ignoramos la línea de cabecera
        reader = csv.reader(file)
        instancias = 0
        days = [] #lista de días
        seasons =[] #lista de estaciones
        winds= [] #lista de viento
        rains=[] #lista de lluvia
        clases=[] #lista de clases

        #Recorremos el fichero linea a linea
        for row in reader:
            instancias+=1 #aumentamos el número de instancias leídas
            days.append(row[0]) #el atributo de la primera columna lo añadimos a días
            seasons.append(row[1]) #el atributo de la segunda columna lo añadimos a estaciones
            winds.append(row[2]) #el atributo de la tercera columna lo añadimos a viento
            rains.append(row[3]) #el atributo de la cuarta columna lo añadimos a lluvia
            clases.append(row[4]) #el atributo de la quinta columnalo añadimos a clases

        atributos = dict(day = days, season = seasons, wind=winds, rain=rains)#creamos un diccionario con los datos del fichero

        print '\nTotal instancias: ',instancias #imprimimos el numero de instancias leidas del fichero

        #Mostramos los posibles valores para cada atributo
        print '\n'
        for i in atributos.iterkeys():
            print 'Atributo ',i, ': ', list(set(atributos.get(i)))
        print 'Clase: ', list(set(clases))
		
		#Mostramos el número de veces que aparece cada clase
        print '\n'
        clasesAux = set(clases)
        for clase in clasesAux:
            print 'Intancias clase ',clase,': ',clases.count(clase)

        #imprimir las instancias con los posibles valores
        file.close()


    def clasifica(self, instancia):
        pass        

    def test(self, fichero):
        pass


if __name__ == '__main__':
    nb = NaiveBayes('train.data',1)