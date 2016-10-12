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
    print dict(country=country.text, capital=country.find("capital").text)