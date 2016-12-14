/*
 * Este fichero ha sido generado para la asignatura SGDI
 * Practica 3, Ejercicio 2
 * Autores: Antonio Calvo Morata y Carlos Congosto Sandoval
 *
 * Antonio Calvo Morata y Carlos Congosto Sandoval declaramos que esta solución es fruto exclusivamente de nuestro
 * trabajo personal. No hemos sido ayudados por ninguna otra persona ni hemos obtenido la solución de fuentes externas,
 * y tampoco hemos compartido nuestra solución con nadie. Declaramos además que no hemos realizado de manera deshonesta
 * ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los resultados de los demás.
 */



/* AGGREGATION PIPELINE */
// 1.- Paises y numero de peliculas, ordenado por numero de peliculas descendente (en empate por nombre pais ascendente)
function agg1(){
	return db.peliculas.aggregate([
		{$unwind:"$pais"},
		{$group:{
			_id:"$pais", 
			cont:{"$sum":1}
		}},	
		{$sort:{cont:-1, _id:1}}]);
}

// 2.- Listado de los 3 tipos de película más populares en 'Emiratos Árabes Unidos' (en caso de
// empate, romper por nombre de película ascendente)
function agg2(){
	return db.usuarios.aggregate([
		{$match:{"direccion.pais":"Emiratos Árabes Unidos"}},
		{$unwind:"$gustos"},
		{$group:{
			_id:"$gustos",
			cont:{"$sum":1}
		}},
		{$sort:{cont:-1,_id:1}},
		{$limit:3}])
}
  
// 3.- Listado (Pais, edad minima-maxima-media) de mayores de 17 años, contando
// únicamente paises con mas de un usuario mayor de 17 años.
function agg3(){
	return db.usuarios.aggregate([
		{$match:{edad:{"$gt":17}}},
		{$group:{
			_id:"$direccion.pais",
			min:{"$min":"$edad"},
			avg:{"$avg":"$edad"},
			max:{"$max":"$edad"},
		}}
		])
}  
  
// 4.- Listado (Titulo pelicula, numero de visualizaciones) de las 10 peliculas 
// más vistas (en caso de empate, romperlo por titulo ascendente)
function agg4(){
	return db.usuarios.aggregate([
		{$unwind:"$visualizaciones"},
		{$group:{
			_id:"$visualizaciones.titulo",
			cont:{"$sum":1}
		}},
		{$sort:{cont:-1,titulo:1}},
		{$limit:10}])
}



  
/* MAPREDUCE */  
  
// 1.- Paises y numero de peliculas
function mr1(){
	return db.peliculas.mapReduce(
		//mapper
		function(){
			this.pais.forEach(function(entry){emit(entry,1);});
		}, 
		//reducer
		function(key,values){
			return Array.sum(values);
		},
		//otros
		{
			out : {inline:1}
		}).find();
}

// 2.- Tipo de pelicula y usuarios de 'Emiratos Árabes Unidos' a los que les gusta
function mr2(){
	return db.usuarios.mapReduce(
		//mapper
		function(){
			this.gustos.forEach(function(entry){emit(entry,1);});
		}, 
		//reducer
		function(key,values){
			return Array.sum(values);
		},
		//otros
		{
			query: { 
				"direccion.pais": "Emiratos Árabes Unidos"
			},
			out : {inline:1}
		}).find();
}

// 3.- Pais - edad minima-maxima-media de mayores de 17 años
function mr3(){
	return db.usuarios.mapReduce(
		//mapper
		function(){
			emit(this.direccion.pais,{avg:this.edad, min: this.edad, max: this.edad, count: 1});
		}, 
		//reducer
		function(key,values){
			var avg2 = 0
			var count2 = 0
			var min2 = Number.MAX_VALUE
			var max2 = Number.MIN_VALUE
			for(var i=1;i<values.length;i++) {
				avg2 += values[i].avg
				count2 += values[i].count
				min2 = min2 < values[i].min ? min2 : values[i].min 
				max2 = max2 > values[i].max ? max2 : values[i].max 
			}
			return {
				avg: avg2,
				min: min2,
				max: max2,
				count: count2
			};
		},
		//otros
		{
			query: { 
				edad: {$gt: 17}
			},
			finalize : function(key, reducedVal){
				reducedVal.avg = reducedVal.avg / reducedVal.count
				return reducedVal
			},
			out : {inline:1}
		}).find();
}

// 4.- Titulo de pelicula y numero de visualizaciones
function mr4(){
	return db.usuarios.mapReduce(
		//mapper
		function(){
			this.visualizaciones.forEach(function(entry){emit(entry.titulo,1);});
		}, 
		//reducer
		function(key,values){
			return Array.sum(values);
		},
		//otros
		{
			out : {inline:1} 
		}).find();
}

