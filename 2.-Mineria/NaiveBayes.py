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
        fieldNames=['day','season','wind','rain','class']
        reader = csv.DictReader(file,fieldNames)


        days = [] #lista de días
        seasons =[] #lista de estaciones
        winds= [] #lista de viento
        rains=[] #lista de lluvia
        classes=[] #lista de clases
        tuplas = []

        #Recorremos el fichero linea a linea
        for row in reader:
            days.append(row['day']) #el atributo de la primera columna lo añadimos a días
            seasons.append(row['season']) #el atributo de la segunda columna lo añadimos a estaciones
            winds.append(row['wind']) #el atributo de la tercera columna lo añadimos a viento
            rains.append(row['rain']) #el atributo de la cuarta columna lo añadimos a lluvia
            classes.append(row['class']) #el atributo de la quinta columnalo añadimos a clases
            for i in range(len(fieldNames)):
                tupla = (row[fieldNames[i]],row['class'])
                tuplas.append(tupla)


        atributos = dict(day = days, season = seasons, wind=winds, rain=rains)#creamos un diccionario con los datos del fichero

        print '\nTotal instancias: ',reader.line_num #imprimimos el numero de instancias leidas del fichero

        #Mostramos los posibles valores para cada atributo
        print '\n'
        classesAux = list(set(classes))
        for i in atributos.iterkeys():
            print 'Atributo ',i, ': ', list(set(atributos.get(i)))
        print 'Clase: ', classesAux
		
		#Mostramos el número de veces que aparece cada clase
        print '\n'
        for clase in classesAux:
            print 'Intancias clase ',clase,': ',classes.count(clase)

        # imprimir las instancias con los posibles valores
        print '\n'
        for c in classesAux:
                for d in set(days):
                    tuplafound =(d,c)
                    print 'Instancias (day = ', d, ', class = ', c, '): ',tuplas.count(tuplafound)
                for s in set(seasons):
                    tuplafound =(s,c)
                    print 'Instancias (season = ', s, ', class = ', c, '): ', tuplas.count(tuplafound)
                for r in set(rains):
                    tuplafound =(r,c)
                    print 'Instancias (rain = ', r, ', class = ', c, '): ', tuplas.count(tuplafound)
                for w in set(winds):
                    tuplafound =(w,c)
                    print 'Instancias (wind = ', w, ', class = ', c, '): ', tuplas.count(tuplafound)
        file.close()




    def clasifica(self, instancia):
        pass        

    def test(self, fichero):
        aciertos = 0
        fallos = 0

        return (aciertos, fallos, aciertos/(aciertos+fallos))


if __name__ == '__main__':
    nb = NaiveBayes('train.data',1)