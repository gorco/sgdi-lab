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
    tfOT = 0
    tfVL = 0
    tfC = 0
    tfL = 0

    def __init__(self, fichero, smooth=1):
        file = open(fichero,'r')
        #next(file, None) #ignoramos la línea de cabecera
        #fieldNames=['day','season','wind','rain','class']
        reader = csv.DictReader(file)

        fieldNames = reader.fieldnames

        atributo1 = [] #lista de días
        atributo2 =[] #lista de estaciones
        atributo3 = [] #lista de viento
        atributo4 =[] #lista de lluvia
        classes=[] #lista de clases
        tuplas = []

        #Recorremos el fichero linea a linea
        for row in reader:
            atributo1.append(row[fieldNames[0]]) #el atributo de la primera columna lo añadimos a días
            atributo2.append(row[fieldNames[1]]) #el atributo de la segunda columna lo añadimos a estaciones
            atributo3.append(row[fieldNames[2]]) #el atributo de la tercera columna lo añadimos a viento
            atributo4.append(row[fieldNames[3]]) #el atributo de la cuarta columna lo añadimos a lluvia
            classes.append(row['class']) #el atributo de la quinta columnalo añadimos a clases
            for i in range(len(fieldNames)):
                tupla = (row[fieldNames[i]],row['class'])
                tuplas.append(tupla)


        atributos = dict(day = atributo1, season = atributo2, wind=atributo3, rain=atributo4)#creamos un diccionario con los datos del fichero

        print '\nTotal instancias: ',reader.line_num-1 #imprimimos el numero de instancias leidas del fichero

        #Mostramos los posibles valores para cada atributo
        print '\n'
        classesAux = list(set(classes))
        for i in atributos.iterkeys():
            print 'Atributo ',i, ': ', set(atributos.get(i))
        print 'Clase: ', classesAux
		
		#Mostramos el número de veces que aparece cada clase
        print '\n'
        for clase in classesAux:
            print 'Intancias clase ',clase,': ',classes.count(clase)

        # imprimir las instancias con los posibles valores
        print '\n'
        for c in classesAux:
                for d in set(atributo1):
                    tuplafound =(d,c)
                    print 'Instancias (day = ', d, ', class = ', c, '): ',tuplas.count(tuplafound)
                for s in set(atributo2):
                    tuplafound =(s,c)
                    print 'Instancias (season = ', s, ', class = ', c, '): ', tuplas.count(tuplafound)
                for r in set(atributo3):
                    tuplafound =(r,c)
                    print 'Instancias (rain = ', r, ', class = ', c, '): ', tuplas.count(tuplafound)
                for w in set(atributo4):
                    tuplafound =(w,c)
                    print 'Instancias (wind = ', w, ', class = ', c, '): ', tuplas.count(tuplafound)
        file.close()



        for atributo in classesAux:
            if smooth:
                at = 1 + math.log(classes.count(atributo),2)
                if atributo == 'very late':
                    self.tfVL = at
                elif atributo == 'late':
                    self.tfL = at
                elif atributo == 'cancelled':
                    self.tfC = at
                else:
                    self.tfOT = at

            else:
                pass

        print 'Very late: ', self.tfVL
        print 'Late: ', self.tfL
        print 'Cancelled: ', self.tfC
        print 'On Time: ', self.tfOT


    def clasifica(self, instancia):
        instancia = dict(instancia)




    def test(self, fichero):
        aciertos = 0
        fallos = 0

        return (aciertos, fallos, aciertos/(aciertos+fallos))


