# coding=utf-8

# Este fichero generado para la asignatura SGDI
# Practica 2, Ejercicio 1. Naive Bayes
# Autores: Antonio Calvo Morata y Carlos Congosto Sandoval

# Antonio Calvo Morata y Carlos Congosto Sandoval declaramos que esta solución es fruto exclusivamente de nuestro
# trabajo personal. No hemos sido ayudados por ninguna otra persona ni hemos obtenido la solución de fuentes externas,
# y tampoco hemos compartido nuestra solución con nadie. Declaramos además que no hemos realizado de manera deshonesta
# ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.


import csv, math, sys


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

        #recorremos todas las líneas leidas
        for row in reader:
            self.listaMain.append(row)#Almacenamos el diccionario leido en la lista de las instancias
            clase = row['class']
            listaClases.append(clase)#alamcenamos las clases en una lista de sólo el atributo clase
            #recorremos todos los atributos de la fila leída
            for i in range(len(fieldNames)-1):
                # almacenamos el diccionario (atributo, clase) en una lista de parejas
                dicc = {fieldNames[i]:row[fieldNames[i]],'class':clase}
                parejas.append(dicc)

        #Imprimimos el número de instancias leídas
        print 'Instancias leidas: ', len(self.listaMain),'\n'

        #Creamos tantos conjuntos como atributos hay
        conjuntos = []
        for lista in range(len(reader.fieldnames)):
            conjuntos.append(set())

        #Almacenamos los distintos valores de los atributos en la lista de conjuntos
        for instancia in self.listaMain:
            cont = 0
            for it in range(len(fieldNames)):
                conjuntos[cont].add((instancia.get(fieldNames[cont])))
                cont+=1

        #imprimimos los posibles  valores para cada atributo
        for c in range(len(fieldNames)-1):
            print 'Atributo ', fieldNames[c],': ',list(conjuntos[c])

        #Imprimimos los posibles valores de clase
        self.clases = list(conjuntos[len(fieldNames)-1])
        print 'Clase: ', self.clases,'\n'

        #Imprimimos los valores de clase con el número de veces que se repite
        for clase in self.clases:
            print 'Instancias clase ', clase, ': ', listaClases.count(clase)
        print '\n'

        #Recorremos los posibles valores de clase
        for c in self.clases:
            #Recorremos la lista de conjuntos de atributos
            for cont in range(len(fieldNames)-1):
                #Recorremos los posibles valores de los atributos
                for atributo in conjuntos[cont]:
                    #Contamos las veces que se repite la tupla (atributo, clase) y lo imprimimos
                    cuantas = parejas.count({fieldNames[cont]:atributo,'class':c})
                    print 'Instancias (', fieldNames[cont], ' = ', atributo, ', class = ', c, '): ', cuantas
                    #Calculamos la probabilidad de la pareja
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
            for key in instancia.keys():#Recorremos todas las palabras clave
                for dic in self.probabilidades: #recorremos todas las probabilidades
                    if dic.get('nombre') == instancia.get(key) and dic.get('clase')==clase:#buscamos la probabilidad de la pareja atributo clase
                        if dic.get('prob')!=0.0: #miramos si es distinto de 0
                            prob -= math.log(dic.get('prob'),2)
            #print 'Clase: ',clase, ' Prob: ',prob
            if prob > probCan: #Miramos si la probabilidad actual es mayor que la candidata
                probCan = prob
                candidata = clase

        return candidata


    def test(self, fichero):
        aciertos = 0 #Numero de aciertos
        fallos = 0 #Numero de fallos
        file = open(fichero, 'r')
        reader = csv.DictReader(file)

        print 'TEST'
        #Recorremos las instancias leidas
        for row in reader:
            clase = row['class']#almacenamos en una variable el valor de la clase
            del row['class'] #eliminamos del diccionario la clase
            print row, '-',clase #Imprimos el diccionario con la clase correcta
            predicha = self.clasifica(row) #Hacemos la llamada a la función clasifica
            print 'Clase predicha: ', predicha #Imprimimos la clase predicha
            if predicha == clase: #comprobamos si ha acertado y mostramos el resultado
                print '\t--> Acierto'
                aciertos+=1

            else:
                print '\t--> Fallo'
                fallos+=1

        return (aciertos, fallos, aciertos/float(aciertos+fallos))#Devolvemos la tupla con los resultados

# Como argumentos recibe:
# argv[1] = Fichero de entrenamiento
# argv[2] = Fichero test (OPCIONAL) si no se pasa argumento coge el nombre argv[1] + _test seguido del formato
# argv[3] = Smooth (OPCIONAL y sólo si se ha especificado argv[2]
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "No se ha especificado el fichero!"
        exit(-1)

    file = sys.argv[1]
    smooth = 1
    if len(sys.argv) == 2:
        testfile = file+"_test"
    else :
        testfile = sys.argv[2]
        if len(sys.argv) == 4:
            smooth = int(sys.argv[3])

    nb = NaiveBayes(file, smooth)
    resultado = nb.test(testfile)
    print 'aciertos: ', resultado[0]
    print 'fallos: ', resultado[1]
    print 'tasa: ', resultado[2]

    #nb.clasifica({'day':'weekday','season':'winter','wind':'high','rain':'heavy'})
