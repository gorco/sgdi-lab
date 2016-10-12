# coding=utf-8

# Este fichero generado para la asignatura SGDI
# Ejercicio B.3, Sesion Guiada 1
# Autores: Antonio Calvo Morata y Carlos Congosto Sandoval
from boto import provider

import eulexistdb.db

db = eulexistdb.db.ExistDB("http://localhost:8080/exist")

# 3- Tuplas (o diccionarios) de países junto con su capital. Atención: Algunas
# capitales son elementos “city” hijos directos de “country”, pero otras
# ciudades están dentro de provincias.

q = """for $country in doc("/db/sgdi/factbook.xml")/mondial/country
return $country"""

r = db.query(q, start=1, how_many=-1)

nodes = r. results
for country in nodes:
    capital = country.find("city")
    if capital is not None:
        print dict(country=country.attrib["name"], capital=capital.find("name").text)
    else:
        capital_code = country.attrib["capital"]
        provinces = country.findall("province")
        for p in provinces:
            city = p.find("city")
            if city is not None and city.attrib["id"] == capital_code:
                print dict(country=country.attrib["name"], capital=p.find("city").find("name").text)





