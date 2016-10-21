# coding=utf-8

# Este fichero generado para la asignatura SGDI
# Ejercicio B, Sesion Guiada 1
# Autores: Antonio Calvo Morata y Carlos Congosto Sandoval

# Antonio Calvo Morata y Carlos Congosto Sandoval declaramos que esta solución es fruto exclusivamente de nuestro
# trabajo personal. No hemos sido ayudados por ninguna otra persona ni hemos obtenido la solución de fuentes externas,
# y tampoco hemos compartido nuestra solución con nadie. Declaramos además que no hemos realizado de manera deshonesta
# ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.

import eulexistdb.db

db = eulexistdb.db.ExistDB("http://localhost:8080/exist")

# Funcion auxiliar para mostrar las listas devueltas por las distintas funciones
def prettyPrint(list):
    for l in list:
        print l

#############################
#
# EJERCICIOS
#
#############################

# 1- Nombres (cadena de texto) de todos los países
def func1():
    result = []
    q = """for $country in doc("/db/sgdi/factbook.xml")/mondial/country
    return $country"""

    r = db.query(q, start=1, how_many=-1)

    nodes = r.results
    for country in nodes:
        result.append(country.attrib["name"])

    return result


# 2- Tuplas (nombre pais, id pais , codigo pais ) con la información de los países.
# También se permite devolver diccionarios Python en lugar de tuplas
def func2():
    result = []
    q = """for $country in doc("/db/sgdi/factbook.xml")/mondial/country
    return <country name="{$country/@name}" id="{$country/@id}" code="{$country/@datacode}"></country>"""

    r = db.query(q, start=1, how_many=-1)

    nodes = r.results
    for country in nodes:
        result.append(dict(name=country.attrib["name"], id=country.attrib["id"], code=country.attrib["code"]))

    return result


# 3- Tuplas (o diccionarios) de países junto con su capital. Atención: Algunas
# capitales son elementos “city” hijos directos de “country”, pero otras
# ciudades están dentro de provincias.
def func3():
    result = []
    q = """for $country in doc("/db/sgdi/factbook.xml")//country
    let $cap := $country/@capital
    return
        <pais>
            {data($country/name)}
            <capital>
               {
                   for $city in doc("/db/sgdi/factbook.xml")//city
                   where $city/@id = $cap
                   return data($city/name)
               }
            </capital>
        </pais>"""

    r = db.query(q, start=1, how_many=-1)

    nodes = r.results
    for country in nodes:
        result.append(dict(country=country.text, capital=country.find("capital").text))

    return result

# 4- Nombres (cadena de texto) de los países que están en más de un continente
def func4():
    result = []
    q = """for $country in doc("/db/sgdi/factbook.xml")//country
        where count($country/encompassed/@continent) > 1
        return $country/name"""

    r = db.query(q, start=1, how_many=-1)

    nodes = r.results
    for country in nodes:
        result.append(country.text)

    return result

# 5- Nombres (cadena de texto) de los países americanos con área total mayor
# de 100000, ordenados en order lexicográfico inverso.
def func5():
    result = []
    q = """for $country in doc("/db/sgdi/factbook.xml")//country
        where $country/encompassed/@continent ="f0_126" and $country/@total_area > 100000
        order by $country/@name descending
        return $country/name[1]""" #$a/name[1] devuelve sólo el primer nombre del país en caso de tener más de
                            # un nombre, por ejemplo con "United States"/"USA"/"states" devuelve sólo USA

    r = db.query(q, start=1, how_many=-1)

    nodes = r.results
    for country in nodes:
        result.append(country.text)

    return result

# 6- Parejas (ciudad, pais ) o diccionarios Python de las ciudades en países con
# inflación superior a 20. Se recomienda obtener todas estas ciudades mediante
# una sola consulta a eXist-db, aunque se permite realizar varias
# consultas anidadas.
def func6():
    result = []
    q = """for $country in doc ("/db/sgdi/factbook.xml")//country
        where $country/@inflation >20
        return
            for $city in $country//city
            return
                <tupla>
                    <pais>
                        {$country/name/text()}
                    </pais>
                    <ciudad>
                        {$city/name/text()}
                    </ciudad>
                </tupla>"""

    r = db.query(q, start=1, how_many=-1)

    nodes = r.results
    for country in nodes:
        result.append(dict(pais=country.find("pais").text, ciudad=country.find("ciudad").text))

    return result


###################################
#
# Probar funciones
#
###################################

print prettyPrint(func6())
