# coding=utf-8

# Este fichero generado para la asignatura SGDI
# Ejercicio B.1, Sesion Guiada 1
# Autores: Antonio Calvo Morata y Carlos Congosto Sandoval

import eulexistdb.db

db = eulexistdb.db.ExistDB("http://localhost:8080/exist")

# 1- Nombres (cadena de texto) de todos los países
q = """for $country in doc("/db/sgdi/factbook.xml")/mondial/country
return $country"""

r = db.query(q, start=1, how_many=-1)

nodes = r. results
for country in nodes:
	print country.attrib["name"]

