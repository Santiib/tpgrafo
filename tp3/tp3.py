# -*- coding: utf-8 -*-
import sys
from grafo import *
from PriorityQueue import * #clase del modulo PriorityQueue con el metodo añadido para ver primero

COEFICIENTE_AMORTIGUACION = 0.85
RANKING_DEFAULT = 0.50

def cargar_articulos(archivo,cantidad_articulos):

    grafo = Grafo(True)
    i = 0

    while i < cantidad_articulos:

        linea = archivo.readline()
        articulo = linea.split(">")[0]
        grafo[articulo] = RANKING_DEFAULT 
        i += 1
        
    archivo.seek(0)
    return grafo

def relacionar_articulos(archivo,grafo,cantidad_articulos):       
    
    j = 0

    while j < cantidad_articulos:

        linea = archivo.readline().rstrip("\n")
        informacion = linea.split(">")
        articulo_principal = informacion[0]
        relaciones = informacion[1].split("<")
        for articulo in relaciones:
            
            if articulo in grafo:
                
                grafo.agregar_arista(articulo_principal,articulo)

        j += 1

def pedir_natural(msg):

    correcto = False
    while not correcto:
        n = raw_input(msg+": ")
        if n.isdigit():
            correcto = True
    return int(n)

def calcular_pagerank(wikipedia_es):


    sumatoria_pageranks = 0
    for articulo in wikipedia_es:

        sumatoria_pageranks += wikipedia_es[articulo]

    
    iteraciones = pedir_natural("Ingrese el valor de k (k > 0)")
    cantidad_vertices = len(wikipedia_es)
    
    while iteraciones > 0:

        for articulo in wikipedia_es:
        
            links = wikipedia_es.incidencias(articulo)
            sumatoria = 0            
            for link in links:

                pagerank_link = wikipedia_es[link]
                relacionados_a_link = len(wikipedia_es.adyacentes(link))
                relacion_actual = pagerank_link/float(relacionados_a_link)
                sumatoria += relacion_actual    

            pagerank_articulo = ((1 - COEFICIENTE_AMORTIGUACION) / cantidad_vertices) + (COEFICIENTE_AMORTIGUACION * sumatoria)
            wikipedia_es[articulo] = pagerank_articulo

        iteraciones -= 1
        
    sumatoria_pageranks = 0
    for articulo in wikipedia_es:

        sumatoria_pageranks += wikipedia_es[articulo]

def consultar_pagerank_articulo(grafo_wikipedia):

    continuar = True
    
    while continuar:

        try:
    
            articulo_interes = raw_input("Ingrese el nombre del articulo: ")
            if articulo_interes == "-1":

                continuar = False

            print grafo_wikipedia[articulo_interes]
            continuar = False

        except KeyError:

            print "El articulo que ingreso no existe, ingrese un articulo valido o -1 para salir"
       

def ver_top_pagerank(grafo_wikipedia):

    limite = len(grafo_wikipedia)
    cantidad = pedir_natural("Cuantos elementos desea ver en el top?: ")
    if cantidad > limite:

        cantidad = limite

    articulos = [articulo for articulo in grafo_wikipedia]
    posicion_actual = 0
    top_articulos = ColaPrioridad()
    for x in range(0,cantidad): #Encolo <cantidad> de articulos al principio, si no podria estar ignorando soluciones

        top_articulos.put((grafo_wikipedia[articulos[x]], articulos[x]))
        posicion_actual+=1
    
    for i in range(posicion_actual, limite):

        articulo_actual = articulos[i]
        pagerank_actual = grafo_wikipedia[articulo_actual]
        ultimo_mejor = top_articulos.first()
        pagerank_ultimo_mejor = ultimo_mejor[0]
        
        if pagerank_actual > pagerank_ultimo_mejor:

            top_articulos.get()
            top_articulos.put((pagerank_actual,articulo_actual))
    
    mejores = list()
    while not top_articulos.empty():
        articulo = top_articulos.get()
        mejores.append(articulo)

    mejores.reverse()
    valor_pagerank = 0
    nombre_articulo = 1
    print ""
    for pos_articulo in range(len(mejores)):
         
        print "{}. {}: {}".format(pos_articulo + 1, mejores[pos_articulo]
                        [nombre_articulo], mejores[pos_articulo][valor_pagerank]) 
    print ""   

def pedir_articulo(grafo, mensaje):

    continuar = True
    
    while continuar:

        articulo = raw_input(mensaje)
        if articulo in grafo:

            continuar = False
            continue

        print "**El articulo ingresado no se encontro en la base de datos, por favor reintentar**"

    return articulo

def buscar_recorrido_minimo(grafo_wikipedia_es):
    
    origen = pedir_articulo(grafo_wikipedia_es,"Ingrese el nombre del articulo de origen: ")
    destino = pedir_articulo(grafo_wikipedia_es,"Ingrese el nombre del articulo de destino: ")
    link_origen_destino = grafo_wikipedia_es.camino_minimo(origen,destino)
    if link_origen_destino:

        print "->".join(link_origen_destino)
    
    else:

        print "No hay links de "+origen+" con destino a "+destino

def centralidad(grafo, k):
	calculados = []
	centralidad = {}
	for v in grafo.vertices:
		for w in grafo.vertices:
			if (not grafo.es_dirigido) and (vertice in calculados):
				continue
			camino = grafo.camino_minimo(v, w)
			if camino is None:
				continue
			for u in camino:
				if u not in centralidad:
					centralidad[u] = 1
				else:
					centralidad[u] += 1
		calculados.append(v)
	print centralidad
	centralidades = sorted(centralidad.items(), key=operator.itemgetter(1)) #devuelve lista de las key ordenadas por su valor
	centralidades.reverse()
	pos = 0
	k_mas_centrales = []
	while pos < k:
		k_mas_centrales.append((centralidades[pos])[0])
		pos += 1
	return k_mas_centrales

def funcion6(grafo):
    raise NotImplementedError()

def funcion7(grafo):
    raise NotImplementedError()
menu = {
        "Calcular pagerank":calcular_pagerank,
        "Ver pagerank de un articulo":consultar_pagerank_articulo,
        "Mostrar top pagerank":ver_top_pagerank,
        "Recorrido minimo de un articulo a otro":buscar_recorrido_minimo,
        "Centralidad":centralidad,
        "<Comando opcional 1>":funcion6,
        "<Comando opcional 2>":funcion7
        }

def abrir_archivo():

    entrada_correcta = False
    while not entrada_correcta:
        try:
            archivo = open(raw_input("Ingrese el nombre del archivo ya parseado: "),"r")
            entrada_correcta = True
        except IOError:
            print "Archivo/directorio inexistente o no se tienen permisos, intente nuevamente"

    return archivo

def main():
    
    if len(sys.argv) > 2 or len(sys.argv) == 1 or not sys.argv[1].isdigit() or int(sys.argv[1]) < 0:
        print "Uso: tp3.py <cantidad_articulos> (cantidad_articulos >= 0)"
        return
    cantidad_articulos = int(sys.argv[1])
    archivo = abrir_archivo()
    grafo_wikipedia_es = cargar_articulos(archivo,cantidad_articulos)
    relacionar_articulos(archivo,grafo_wikipedia_es,cantidad_articulos)
    archivo.close()
    print "Escoja una opcion, o -1 para finalizar el programa"
    
    opciones = menu.keys()
    entrada = 0
    while entrada != "-1":

        for i in range (len(opciones)):
            print str(i+1)+") "+opciones[i]

        entrada = raw_input("Ingrese una opcion: ")
       
        if entrada == "-1":
            continue
        
        if not entrada.isdigit() or int(entrada) < 1 or int(entrada) > len(opciones):
            entrada = 0
            print "Debe ingresar un numero entre 1 y "+str(len(opciones))
            continue

        menu[opciones[int(entrada) - 1]](grafo_wikipedia_es)
            
main()
