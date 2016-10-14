# coding=utf-8

# Este fichero generado para la asignatura SGDI
# Ejercicio B, Sesion Guiada 1
# Autores: Antonio Calvo Morata y Carlos Congosto Sandoval

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
    q = """for $c in doc("/db/sgdi/factbook.xml")//country
    let $cap := $c/@capital
    return
        <pais>
            {data($c/name)}
            <capital>
               {
                   for $ciudad in doc("/db/sgdi/factbook.xml")//city
                   where $ciudad/@id = $cap
                   return data($ciudad/name)
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

###################################
#
# Probar funciones
#
###################################

print prettyPrint(func4())