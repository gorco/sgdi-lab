/*
* CABECERA AQUI
*/



/* AGGREGATION PIPELINE */
// 1.- Paises y numero de peliculas, ordenado por numero de peliculas descendente (en empate por nombre pais ascendente)
function agg1(){
	 db.peliculas.aggregate([{$unwind:"$pais"},
							{$group:{"_id":"$pais",num:{"$sum":1}}},
							{$project:{_id:0,pais:"$_id",num:1}},
							{$sort:{num:-1,pais:1}}])                                    
}

// 2.- Listado de los 3 tipos de película más populares en 'Emiratos Árabes Unidos' (en caso de
// empate, romper por nombre de película ascendente)
function agg2(){
   db.usuarios.aggregate([{$match:{"direccion.pais":"Emiratos Árabes Unidos"}},
						{$unwind:"$gustos"},
						{$group:{"_id":"$gustos",cont:{"$sum":1}}},
						{$project:{_id:0,gusto:"$_id",cont:1}},
						{$sort:{cont:-1,gusto:1}},
						{$limit:10}])
}
  
// 3.- Listado (Pais, edad minima-maxima-media) de mayores de 17 años, contando
// únicamente paises con mas de un usuario mayor de 17 años.
function agg3(){
  /* */
}  
  
  
// 4.- Listado (Titulo pelicula, numero de visualizaciones) de las 10 peliculas 
// más vistas (en caso de empate, romperlo por titulo ascendente)
function agg4(){
  db.usuarios.aggregate([{$unwind:"$visualizaciones"},
					{$group:{"_id":"$visualizaciones.titulo",visualizaciones:{"$sum":1}}},
					{$project:{_id:0,pelicula:"$_id",visualizaciones:1}},
					{$sort:{visualizaciones:-1,pelicula:1}},
					{$limit:10}])   
}



  
/* MAPREDUCE */  
  
// 1.- Paises y numero de peliculas
function mr1(){
	/* */
}

// 2.- Tipo de pelicula y usuarios de 'Emiratos Árabes Unidos' a los que les gusta
function mr2(){
	/* */
}

// 3.- Pais - edad minima-maxima-media de mayores de 17 años
function mr3(){
	/* */
}

// 4.- Titulo de pelicula y numero de visualizaciones
function mr4(){
	/* */
}

