# coding=utf-8

# Este fichero generado para la asignatura SGDI
# Practica 3, Consultas
# Autores: Antonio Calvo Morata y Carlos Congosto Sandoval

# Antonio Calvo Morata y Carlos Congosto Sandoval declaramos que esta solución es fruto exclusivamente de nuestro
# trabajo personal. No hemos sido ayudados por ninguna otra persona ni hemos obtenido la solución de fuentes externas,
# y tampoco hemos compartido nuestra solución con nadie. Declaramos además que no hemos realizado de manera deshonesta
# ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.
from bson import ObjectId
from pymongo import MongoClient


# 1. Fecha y título de las primeras 'n' peliculas vistas por el usuario 'user_id'.
# >>> usuario_peliculas( 'fernandonoguera', 3 )
def usuario_peliculas(user_id, n):
    client = MongoClient()
    db = client['sgdi_pr3']
    user = db.usuarios.find({"_id":"fernandonoguera"},{"visualizaciones":{"$slice":n}})
    for u in user:
        for v in u['visualizaciones']:
            print 'Titulo: ', v['titulo']
            print 'Fecha: ', v['fecha']
    client.close()
    
   
# 2. _id, nombre y apellidos de los primeros 'n' usuarios a los que les gusten 
# varios tipos de película ('gustos') a la vez.
# >>> usuarios_gustos(  ['terror', 'comedia'], 5  )
def usuarios_gustos(gustos, n):
    client = MongoClient()
    db = client['sgdi_pr3']
    users = db.usuarios.find({"gustos":{"$all":gustos}}).limit(5)
    for user in users:
        print user['_id']
        print user['gustos']
    client.close()
    

# 3. Numero de películas producidas (aunque sea parcialmente) en un pais 
# >>> num_peliculas( 'España' )
def num_peliculas(pais):
    client = MongoClient()
    db = client['sgdi_pr3']
    peliculas = db.peliculas.find({"pais": pais}).count()
    print peliculas

    client.close()


    
# 4. _id de los usuarios que viven en tipo de via y en un piso concreto.
# >>> usuarios_via_num('Plaza', 1)
def usuarios_via_num(tipo_via, numero):
    client = MongoClient()
    db = client['sgdi_pr3']
    users = db.usuarios.find({"direccion.tipo_via":tipo_via},{"numero":numero})
    for user in users:
        print user

    client.close()


# 5. _id de usuario de un determinado sexo y edad en un rango
# >>> usuario_sexo_edad('M', 50, 80)
def usuario_sexo_edad( sexo, edad_min, edad_max ):
    client = MongoClient()
    db = client['sgdi_pr3']
    users = db.usuarios.find({'sexo': 'M','edad':{'$gte':edad_min, '$lte':edad_max}})
    for user in users:
        print user['_id'],' ',user['edad']

    client.close()

# 6. Nombre, apellido1 y apellido2 de los usuarios cuyos apellidos coinciden,
# ordenado por edad ascendente
# >>> usuarios_apellidos()
def usuarios_apellidos():#falta
    client = MongoClient()
    db = client['sgdi_pr3']
    users = db.usuarios.find()

    client.close()
    
# 7.- Titulo de las peliculas cuyo director tienen un nombre que empieza por
# un prefijo
# >>> pelicula_prefijo( 'Yol' )
def pelicula_prefijo( prefijo ):
    client = MongoClient()
    db = client['sgdi_pr3']
    peliculas = db.peliculas.find({'director': {'$regex': '^'+prefijo}})

    for peli in peliculas:
        print peli['titulo']

    client.close()

pelicula_prefijo( 'Yol' )

    

# 8.- _id de usuarios con exactamente 'n' gustos cinematográficos, ordenados por
# edad descendente
# >>> usuarios_gustos_numero( 6 )
def usuarios_gustos_numero(n):
    client = MongoClient()
    db = client['sgdi_pr3']
    usuarios = db.usuarios.find({'gustos':{'$size':n}})

    for usuario in usuarios:
        print usuario['_id']

    client.close()

    
# 9.- usuarios que vieron una determinada pelicula en un periodo concreto
# >>> usuarios_vieron_pelicula( '583ef650323e9572e2812680', '2015-01-01', '2016-12-31' )
def usuarios_vieron_pelicula(id_pelicula, inicio, fin):#falta
    client = MongoClient()
    db = client['sgdi_pr3']
    usuarios = db.usuarios.find({'visualizaciones._id':ObjectId(id_pelicula)})#id bien

    for user in usuarios:
        print user['_id']
        print user['visualizaciones']

    client.close()


#usuarios_vieron_pelicula( '583ef651323e9572e2813e64', '2015-01-01', '2016-12-31' )

