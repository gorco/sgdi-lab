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
    #Conexión con la BBDD
    client = MongoClient()
    db = client['sgdi_pr3']

    #Consulta
    user = db.usuarios.find_one({"_id":user_id},{"visualizaciones":{"$slice":n}})
    #Mostrar resultados de la consulta
    for v in user['visualizaciones']:
        print 'Titulo: ', v['titulo']
        print 'Fecha: ', v['fecha']

    #Cierre de la conexión
    client.close()


# 2. _id, nombre y apellidos de los primeros 'n' usuarios a los que les gusten 
# varios tipos de película ('gustos') a la vez.
# >>> usuarios_gustos(  ['terror', 'comedia'], 5  )
def usuarios_gustos(gustos, n):
    # Conexión con la BBDD
    client = MongoClient()
    db = client['sgdi_pr3']

    # Consulta
    users = db.usuarios.find({"gustos":{"$all":gustos}}).limit(5)
    # Mostrar resultados de la consulta
    for user in users:
        print user['_id'], '\t', user['nombre'], ' ', user['apellido1'], ' ', user['apellido2']

    # Cierre de la conexión
    client.close()
    
# 3. Numero de películas producidas (aunque sea parcialmente) en un pais
# >>> num_peliculas( 'España' )
def num_peliculas(pais):
    # Conexión con la BBDD
    client = MongoClient()
    db = client['sgdi_pr3']

    # Consulta
    peliculas = db.peliculas.find({"pais": pais}).count()
    # Mostrar resultados de la consulta
    print 'Peliculas producidas en ', pais,': ',peliculas

    # Cierre de la conexión
    client.close()

    
# 4. _id de los usuarios que viven en tipo de via y en un piso concreto.
# >>> usuarios_via_num('Plaza', 1)
def usuarios_via_num(tipo_via, numero):
    # Conexión con la BBDD
    client = MongoClient()
    db = client['sgdi_pr3']

    # Consulta
    users = db.usuarios.find({"direccion.tipo_via":tipo_via},{"numero":numero})
    # Mostrar resultados de la consulta
    for user in users:
        print user['_id']

    client.close()


# 5. _id de usuario de un determinado sexo y edad en un rango
# >>> usuario_sexo_edad('M', 50, 80)
def usuario_sexo_edad( sexo, edad_min, edad_max ):
    # Conexión con la BBDD
    client = MongoClient()
    db = client['sgdi_pr3']
    # Consulta
    users = db.usuarios.find({'sexo': 'M','edad':{'$gte':edad_min, '$lte':edad_max}})
    # Mostrar resultados de la consulta
    for user in users:
        print user['_id']

    # Cierre de la conexión
    client.close()

# 6. Nombre, apellido1 y apellido2 de los usuarios cuyos apellidos coinciden,
# ordenado por edad ascendente
# >>> usuarios_apellidos()
def usuarios_apellidos():
    # Conexión con la BBDD
    client = MongoClient()
    db = client['sgdi_pr3']

    #Consulta
    users = db.usuarios.find({'$where': 'this.apellido1 == this.apellido2'}).sort('edad',1)
    # Mostrar resultados de la consulta
    for u in users:
        print u['nombre'],' ',u['apellido1'],' ',u['apellido2']

    # Cierre de la conexión
    client.close()


# 7.- Titulo de las peliculas cuyo director tienen un nombre que empieza por
# un prefijo
# >>> pelicula_prefijo( 'Yol' )
def pelicula_prefijo( prefijo ):
    # Conexión con la BBDD
    client = MongoClient()
    db = client['sgdi_pr3']

    # Consulta
    peliculas = db.peliculas.find({'director': {'$regex': '^'+prefijo}})
    # Mostrar resultados de la consulta
    for peli in peliculas:
        print peli['titulo']

    # Cierre de la conexión
    client.close()


# 8.- _id de usuarios con exactamente 'n' gustos cinematográficos, ordenados por
# edad descendente
# >>> usuarios_gustos_numero( 6 )
def usuarios_gustos_numero(n):
    # Conexión con la BBDD
    client = MongoClient()
    db = client['sgdi_pr3']

    # Consulta
    usuarios = db.usuarios.find({'gustos':{'$size':n}}).sort('edad',1)
    # Mostrar resultados de la consulta
    for usuario in usuarios:
        print usuario['_id']

    # Cierre de la conexión
    client.close()

# 9.- usuarios que vieron una determinada pelicula en un periodo concreto
# >>> usuarios_vieron_pelicula( '583ef650323e9572e2812680', '2015-01-01', '2016-12-31' )
def usuarios_vieron_pelicula(id_pelicula, inicio, fin):
    # Conexión con la BBDD
    client = MongoClient()
    db = client['sgdi_pr3']

    # Consulta
    usuarios = db.usuarios.find({'visualizaciones':
                                     {'$elemMatch': {'_id':ObjectId(id_pelicula),'fecha':{'$gte':inicio, '$lte':fin}}}})
    # Mostrar resultados de la consulta
    for user in usuarios:
        print user['_id']

    # Cierre de la conexión
    client.close()



