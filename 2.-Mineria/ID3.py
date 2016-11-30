# coding=utf-8

# Este fichero generado para la asignatura SGDI
# Practica 2, Ejercicio 2.ID3
# Autores: Antonio Calvo Morata y Carlos Congosto Sandoval

# Antonio Calvo Morata y Carlos Congosto Sandoval declaramos que esta solución es fruto exclusivamente de nuestro
# trabajo personal. No hemos sido ayudados por ninguna otra persona ni hemos obtenido la solución de fuentes externas,
# y tampoco hemos compartido nuestra solución con nadie. Declaramos además que no hemos realizado de manera deshonesta
# ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.

import csv, math, sys

class Nodo:pass

class Hoja(Nodo):
    def __init__(self, valor):
        self.nodo = valor

class NodoInterno(Nodo):
    def __init__(self, valor):
        self.nodo = valor
        self.aristas=[]

    def aniadeHijo(self, valor, nodo):
        self.aristas.append((valor,nodo))


class ID3(object):
    conjuntos = []  # Lista que tendrá las listas de atributos
    instancias = [] # número de instancias leídas
    fieldNames = []
    reader = None
    arbol = None

    #Descubre el valor mayoritario de clase
    def mayoritaria(self,instancias):
        may = 0 #Numero de veces que se repite la mayoritari
        clase = ''#Clase mayoritaria
        #Recorremos los posibles valores de clase
        for c in self.conjuntos[len(self.conjuntos)-1]:
            rep = 0#Numero de repeticiones de la clase
            #Recorremos las instancias
            for ins in instancias:
                #Contamos las instancias con class igual a la clase
                if (ins.get('class')==c):
                    rep+=1
            #Actualizamos los valores de mayoritaria
            if rep > may:
                may = rep
                clase = c

        return clase

    #función que mira si el valor de clase es único
    def unico(self,instancias):
        unico = True#La clase es unica
        i = 1 # Iterador
        #Tomamos el primer valor de clase de las instancias
        clase = instancias[0].get('class')
        #Recorremos las instancias mientras el valor de clase sea único
        while unico and i < len(instancias):
            if self.instancias[i].get('class') != clase:
                unico = False
            i+=1
        return unico

    #Crea una lista con las instancias que cumplen con el atributo y el valor de dicho atributo
    def particion(self, instancias,  atributo, valor):
        ret =[]#lista de instancias
        #Recorremos las instancias
        for instancia in instancias:
            #Comprobamos que la instancia cumple la condicion
            if instancia.get(atributo)==valor:
                ret.append(instancia)#Si cumple lo añadimos a la lista
        return ret

    #funcion que crea el arbol de decisión
    def tdidt (self, instancias, claves):
        cp = self.mayoritaria(instancias)#Buscamos la clase mayoritaria
        #Si la clase es única
        if self.unico(instancias):
            return Hoja(instancias[0].get('class'))
        #Si la lista de claves es vacía
        elif len(claves) == 0:
            return Hoja(cp)
        else:
            atributo = self.selectAtribute(claves,instancias)#Buscamos el atributo con la menor entropía
            n = NodoInterno(atributo)#Nos creamos un nodo interno con el atributo
            #Recorremos los valores de dicho atributo
            for valor in self.conjuntos[self.fieldNames.index(atributo)]:
                cj = self.particion(instancias, atributo, valor)#Conjunto con el valor del atributo que trabajamos
                if len(cj)==0: #si es vacio creamos una hoja
                    nh = Hoja(cp)
                else:
                    clavesAux = [] #lista de atributos auxiliar
                    for clave in claves:
                        if clave != atributo:#Almacenamos todos los atributos en la lista salvo el atributo con el que trabajamos
                            clavesAux.append(clave)
                    #Hacemos la llamada recursiva y creamos el hijo
                    nh = self.tdidt(cj,clavesAux)
                n.aniadeHijo(nh, valor)

            return n

    #Averiguar el atributo con la menor entropía
    def selectAtribute(self,atributos,instancias):
        #Si existe el atributo class lo eliminamos
        if atributos.count('class')>0:
            atributos.remove('class')

        EntropiaMin = sys.maxint #Indicador de la menor entropía
        Raiz = ''#Atributo con la menor entropía
        #Recorremos los atributos
        for atributo in atributos:
            Entropia = 0 #Entropía del atributo
            #Recorremos los valores del atributo
            for valor in self.conjuntos[self.fieldNames.index(atributo)]:
                listAux = [] #Lista auxiliar
                entropiaAux = 0 #entropia de cada valor
                #Recorremos las instancias
                for instancia in instancias:
                    if instancia.get(atributo) == valor:#Si el valor del atributo es correcto se añade a la lisat
                        listAux.append(instancia)
                #Recorremos los valores de clase
                for clase in self.conjuntos[len(self.conjuntos) - 1]:
                    cont = 0.0 #Contador
                    for ins in listAux: #Recorremos la lista auxiliar de instancias
                        if ins.get('class') == clase:
                            cont += 1.0
                    if len(listAux) == 0:
                        t = 0
                    else:
                        t = cont / len(listAux)
                    #Calculamos la entropia del valor del atributo
                    if t == 0.0:
                        entropiaAux = 0.0
                    else:
                        entropiaAux -= t * math.log(t, 2)
                Entropia += (len(listAux) / float(self.reader.line_num - 1)) * entropiaAux #Calculamos la entropia el atributo
            #Actualizamos los datos de menor entropía
            if Entropia < EntropiaMin:
                EntropiaMin = Entropia
                Raiz = atributo
        return Raiz

    def __init__(self, fichero):
        file = open(fichero, 'r')
        self.reader = csv.DictReader(file)
        self.fieldNames = self.reader.fieldnames  # creamos una lista con los nombres de los atributos


        # Creamos tantos conjuntos como columnas hay en el fichero
        for i in range(len(self.fieldNames)):
            self.conjuntos.append(set())

        # leemos y guardamos los datos del fichero
        for row in self.reader:
            self.instancias.append(row)
            for i in range(len(row)):
                self.conjuntos[i].add(row[self.fieldNames[i]])

        print '\nTotal instancias: ', self.reader.line_num-1  # imprimimos el numero de instancias leidas del fichero

        self.arbol = self.tdidt(self.instancias, self.fieldNames)



    def clasifica(self, instancia):
        arbol = self.arbol

        while arbol.__class__!=Hoja:
            for arista in arbol.aristas:
                if arista[1] == instancia.get(arbol.nodo):
                    arbol = arista[0]

        return arbol.nodo

    def test(self, fichero):
        aciertos = 0
        fallos = 0

        file = open(fichero, 'r')
        reader = csv.DictReader(file)

        print 'TEST'
        for row in reader:
            clase = row['class']
            del row['class']
            print row, '-', clase
            predicha = self.clasifica(row)
            print 'Clase predicha: ', predicha
            if predicha == clase:
                print '\t--> Acierto'
                aciertos += 1

            else:
                print '\t--> Fallo'
                fallos += 1

        return (aciertos, fallos, aciertos / float(aciertos + fallos))

    def save_tree(self, fichero):
        self.lines = set()
        self.nodos = set()
        file = open(fichero,'w')
        file.write('digraph tree {\n')
        arb = self.arbol
        self.imprime(arb,file)

        for n in self.nodos:
            file.write(n)

        for a in self.lines:
            line = '"'+a[0]+'" -> "'+a[2]+'" [label = "'+a[1]+'"];\n'
            file.write(line)
        file.write('}\n')
        file.close()

    def imprime(self, arbol, file):

        if arbol.__class__==Hoja:
            line = '"'+arbol.nodo+'" [label = "'+arbol.nodo+'"];\n'
            self.nodos.add(line)
        else:
            line = '"'+arbol.nodo + '" [label = "' + arbol.nodo + '", shape = "box"];\n'
            self.nodos.add(line)
            for arista in arbol.aristas:
                self.lines.add((arbol.nodo, arista[1],arista[0].nodo))
                self.imprime(arista[0],file)

# Como argumentos recibe:
# argv[1] = Fichero de entrenamiento
# argv[2] = Fichero test (OPCIONAL) si no se pasa argumento coge el nombre argv[1] + _test seguido del formato
# argv[3] = Smooth (OPCIONAL y sólo si se ha especificado argv[2]
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "No se ha especificado el fichero!"
        exit(-1)

    file = sys.argv[1]
    if len(sys.argv) == 2:
        testfile = file+"_test"
    else :
        testfile = sys.argv[2]

    id3 = ID3(file)
    resultado = id3.test(testfile)
    id3.save_tree('train.dot')
    print 'aciertos: ', resultado[0]
    print 'fallos: ', resultado[1]
    print 'tasa: ', resultado[2]

    #id3.clasifica({'day': 'weekday', 'season': 'winter', 'wind': 'high', 'rain': 'heavy'})

