# -*- coding: utf-8 -*-
import sys
import operator
from grafo import *
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

def calcular_pagerank(wikipedia_es, k):


    sumatoria_pageranks = 0
    for articulo in wikipedia_es:
        sumatoria_pageranks += wikipedia_es[articulo]

    print sumatoria_pageranks
    
    iteraciones = k
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

            pagerank_articulo = (1 - COEFICIENTE_AMORTIGUACION / cantidad_vertices) + (COEFICIENTE_AMORTIGUACION * sumatoria)
            wikipedia_es[articulo] = pagerank_articulo
        iteraciones -= 1
        
    sumatoria_pageranks = 0
    for articulo in wikipedia_es:
        sumatoria_pageranks += wikipedia_es[articulo]

def consultar_pagerank_articulo(grafo, articulo):
	continuar = True
	while continuar:
		try:
			articulo_interes = articulo
			if articulo_interes == "-1":
				continuar = False
			return grafo[articulo_interes]
			continuar = False
		except KeyError:
			print "El articulo que ingreso no existe, ingrese un articulo valido o -1 para salir"

			
def abrir_archivo(nombre):

    entrada_correcta = False
    while not entrada_correcta:
        try:
            archivo = open(nombre,"r")
            entrada_correcta = True
        except IOError:
            print "Archivo/directorio inexistente o no se tienen permisos, intente nuevamente"

    return archivo

def verificar_pagerank(archivo, k, dicc):
	a = abrir_archivo(archivo)
	g = cargar_articulos(a,k)
	calcular_pagerank(g, 1000) #por defecto iterar 1000 veces
	for articulo in dicc:
		if abs(dicc[articulo] - g[articulo]) < 0.2: #margen de error
			print "OK PR de "+articulo
			continue
		else:
			print "error en PR de "+articulo
	a.close()
	del g
	
	
def main():
	d1 = {'A':0.5, 'B':0.5}
	d2 = {'A':7.8, 'B':4.11, 'C':8.2, 'D':0.78}
	d3 = {'A':5.25, 'B':5.25, 'C':5.25, 'D':5.25}
	d4 = {'A':7.53, 'B':7.19, 'C':3.84, 'D':2.42}
	dicc = [d1, d2, d3, d4]
	prueba = 1
	for d in dicc:
		k = 4
		if prueba == 1:
			k = 2
		print "Calculado grafo"+str(prueba)
		verificar_pagerank('articulos'+str(prueba)+'.txt', k, d)
		prueba += 1

main()
