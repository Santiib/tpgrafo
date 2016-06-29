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

def calcular_pagerank(wikipedia_es, iter):


    sumatoria_pageranks = 0
    for articulo in wikipedia_es:
        sumatoria_pageranks += wikipedia_es[articulo]

    print sumatoria_pageranks
    
    iteraciones = iter
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


def abrir_archivo(archivo):

    entrada_correcta = False
    while not entrada_correcta:
        try:
            archivo = open(archivo,"r")
            entrada_correcta = True
        except IOError:
            print "Archivo/directorio inexistente o no se tienen permisos, intente nuevamente"

    return archivo


def hacer_calculo(cant_art, archivo, iter, resultados):
	cantidad_articulos = cant_art
	archivo = abrir_archivo(archivo)
	grafo_wikipedia_es = cargar_articulos(archivo,cantidad_articulos)
	relacionar_articulos(archivo,grafo_wikipedia_es,cantidad_articulos)
	archivo.close()
	calcular_pagerank(grafo_wikipedia_es, iter)
	for articulo in resultados:
		PR = grafo_wikipedia_es[articulo]
		if abs(resultados[articulo] - PR) < 0.2: #margen de error
			print "OK"
		else:
			print PR
			print "error en PR de "+articulo	
	
	
def main():
	d1 = {'A':3.85, 'B':3.85}
	d2 = {'A':7.8, 'B':4.11, 'C':8.2, 'D':0.78}
	d3 = {'A':5.25, 'B':5.25, 'C':5.25, 'D':5.25}
	d4 = {'A':7.53, 'B':7.19, 'C':3.84, 'D':2.42}
	diccs = [d1, d2, d3, d4]
	archivos = ['articulos1.txt','articulos2.txt','articulos3.txt','articulos4.txt']
	numero = 1
	for d in diccs:
		k = 4
		print "Calculando prueba "+str(numero)
		if numero == 1:
			k = 2
		hacer_calculo(k, archivos[numero-1], 40, d)
		numero += 1

            
main()