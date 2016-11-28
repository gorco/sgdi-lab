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
    def __init__(self, atributo):
        self.a = atributo

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

    def mayoritaria(self):
        may = 0
        clase = ''
        for c in self.conjuntos[len(self.conjuntos)-1]:
            rep = 0
            for ins in self.instancias:
                if (ins.get('class')==c):
                    rep+=1
            if rep > may:
                may = rep
                clase = c
        return clase

    def unico(self):
        unico = True
        i = 1
        clase = self.instancias[0].get('class')
        while unico and i < len(self.instancias):
            if self.instancias[i].get('class') != clase:
                unico = False
            i+=1
        return unico

    def particion(self, instancias,  atributo, valor):
        ret =[]
        for instancia in instancias:
            if instancia.get(atributo)==valor:
                ret.append(instancia)
        return ret

    def tdidt (self, instancias, claves):
        print claves
        cp = self.mayoritaria()
        if self.unico():
            return Hoja(instancias[0].get('class'))
        elif len(claves) == 0:
            return Hoja(cp)
        else:
            atributo = self.selectAtribute(claves)
            n = NodoInterno(atributo)
            print 'claves 2', claves
            print 'quier borrar: ',atributo

            for valor in self.conjuntos[self.fieldNames.index(atributo)]:
                print valor
                cj = self.particion(instancias, atributo, valor)
                if len(cj)==0:
                    nh = Hoja(cp)
                else:
                    claves.remove(atributo)
                    nh = self.tdidt(cj,claves)
                n.aniadeHijo(nh, valor)

                return n


    def selectAtribute(self,fieldNames):
        ##Averiguar el atributo con la menor entropía entropia
        EntropiaMin = sys.maxint
        Raiz = ''
        for i in range(len(fieldNames) - 1):
            Entropia = 0
            for valor in self.conjuntos[i]:
                listAux = []
                entropiaAux = 0
                for instancia in self.instancias:
                    if instancia.get(self.fieldNames[i]) == valor:
                        listAux.append(instancia)
                # print listAux
                for clase in self.conjuntos[len(self.conjuntos) - 1]:
                    cont = 0.0
                    for ins in listAux:
                        if ins.get('class') == clase:
                            cont += 1.0
                    if len(listAux) == 0:
                        t = 0
                    else:
                        t = cont / len(listAux)
                    if t == 0.0:
                        entropiaAux = 0.0
                    else:
                        entropiaAux -= t * math.log(t, 2)
                Entropia += (len(listAux) / float(self.reader.line_num - 1)) * entropiaAux
            # print self.fieldNames[i], ':', Entropia
            if Entropia < EntropiaMin:
                EntropiaMin = Entropia
                Raiz = self.fieldNames[i]
                # print 'raiz = ',Raiz
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

        arbol = self.tdidt(self.instancias, self.fieldNames)
        

    def clasifica(self, instancia):
        pass

    def test(self, fichero):
        pass

    def save_tree(self, fichero):
        pass
