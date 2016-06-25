# -*- coding: utf-8 -*-
import sys
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

def calcular_pagerank(wikipedia_es):


    sumatoria_pageranks = 0
    for articulo in wikipedia_es:
        sumatoria_pageranks += wikipedia_es[articulo]

    print sumatoria_pageranks
    
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

def consultar_pagerank_articulo(grafo):
    raise NotImplementedError()

def ver_top_pagerank(grafo):
    raise NotImplementedError()

def buscar_recorrido_minimo(grafo):
    raise NotImplementedError()

def centralidad(grafo):
    raise NotImplementedError()

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
