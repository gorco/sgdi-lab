# coding=utf-8

# Este fichero generado para la asignatura SGDI
# Ejercicio B.2, Sesion Guiada 1
# Autores: Antonio Calvo Morata y Carlos Congosto Sandoval

import eulexistdb.db

db = eulexistdb.db.ExistDB("http://localhost:8080/exist")

# 2- Tuplas (nombre pais, id pais , codigo pais ) con la información de los países.
# También se permite devolver diccionarios Python en lugar de tuplas
q = """for $country in doc("/db/sgdi/factbook.xml")/mondial/country
return <country name="{$country/@name}" id="{$country/@id}" code="{$country/@datacode}"></country>"""

r = db.query(q, start=1, how_many=-1)

nodes = r. results
for country in nodes:
    print dict(name=country.attrib["name"], id=country.attrib["id"], code=country.attrib["code"])
