# coding=utf-8

# Este fichero generado para la asignatura SGDI
# Practica 1 MapReduce Y Spark, Ejercicio D.1
# Autores: Antonio Calvo Morata y Carlos Congosto Sandoval

# Antonio Calvo Morata y Carlos Congosto Sandoval declaramos que esta solución es fruto exclusivamente de nuestro
# trabajo personal. No hemos sido ayudados por ninguna otra persona ni hemos obtenido la solución de fuentes externas,
# y tampoco hemos compartido nuestra solución con nadie. Declaramos además que no hemos realizado de manera deshonesta
# ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.

import sys
from pysparkling import Context


# sys.argv debe contener el nombre de fichero a procesar
if len(sys.argv) != 2:
    print "Falta el fichero!"
    exit(-1)

path = sys.argv[1]

for i in range(2, len(sys.argv)):
    path += ","+sys.argv[i]

sc = Context()
lines = sc.textFile(path)

fallos = []

def compruebayMapea(x):
    line = x.split('\"')
    if len(line) != 3:  # consideramos que la petición no tiene comillas dobles. patron elegido host - - [fecha], petición,  codigo tamaño
        fallos.append(x) #introducimos la línea errónea en una lista
        return 'xxx', (0, 0, 0)#tupla en caso de error. Suponemos que no hay host con nombre 'xxx'
    else:
        parte1 = line[0].split('- -')#separamos el nombre del host de la fecha
        if len(parte1) != 2:#comprobamos que existe en la parte1 de la línea host y fecha
            fallos.append(x)
            return 'xxx', (0, 0, 0)
        else:
            parte3 = line[2].split()
            if len(parte3) != 2:
                fallos.append(x)
                return 'xxx', (0, 0, 0)
            else:
                host = parte1[0].encode('utf-8') #nos quedamos con el host
                tam = parte3[1] #nos quedamos con el tamaño de la petición
                error = 0 #Variable que indica si da un error o no 0 no error
                if tam == '-': #miramos si el tamaño está indicado por '-' , si es cierto, entonces 0
                    tam = 0
                if int(parte3[0]) >= 400:#comprobamos si el codigo devueltgo es mayor de 400
                    error = 1
                return host, (1, int(tam), error)#devolvemos la tupla con los datos buenos



def sumaTodo(x, y):
    peticiones = x[0]+y[0]
    size = x[1]+y[1]
    errores = x[2]+y[2]
    return (peticiones, size, errores)


datos = (
        lines.map(compruebayMapea)  # comprobamos el formato de las líneas y guardamos la informacion relevante
        .filter(lambda x: x[0] != 'xxx') #filtramos por las entradas incorrectas
        .reduceByKey(sumaTodo)#sumamos los valores por campos
        .map(lambda x: (x[0], x[1])) #agrupamos los resultados
)

output = datos.collect()
for o in output:
     print o

#imprimimos el log de fallos
print "Fallos en el fichero:"
for f in fallos:
    print f
