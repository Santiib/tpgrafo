import sys
from grafo import *

def cargar_articulos(archivo,cantidad_articulos):

    grafo = Grafo(True)
    i = 0

    while i < cantidad_articulos:
        linea = archivo.readline()
        articulo = linea.split(">")[0]
        grafo[articulo] = None #Deberia poner el pagerank?
        i += 1
        
    archivo.seek(0)
    return grafo

def relacionar_articulos(archivo,grafo,cantidad_articulos):       
    
    j = 0

    while j < cantidad_articulos:

        linea = archivo.readline()
        informacion = linea.split(">")
        articulo_principal = informacion[0]
        relaciones = informacion[1].split("<")
        for articulo in relaciones:
            if articulo in grafo:
                grafo.agregar_arista(articulo_principal,articulo)

        j += 1

def funcion1():
    raise NotImplementedError()

def funcion2():
    raise NotImplementedError()

def funcion3():
    raise NotImplementedError()

def funcion4():
    raise NotImplementedError()

def funcion5():
    raise NotImplementedError()

def funcion6():
    raise NotImplementedError()

def funcion7():
    raise NotImplementedError()
menu = {
        "Calcular pagerank K":funcion1,
        "Ver pagerank de un artículo":funcion2,
        "Mostrar top pagerank":funcion3                                                        ,
        "Recorrido minimo de un articulo a otro":funcion4,
        "Centralidad":funcion5,
        "<Comando opcional 1>":funcion6
        "<Comando opcional 2>":funcion7
        }

def main():
    
    if len(sys.argv) > 2 or len(sys.argv) == 1 or not sys.argv[1].isdigit() or int(sys.argv[1]) < 0:
        print "Uso: tp3.py <cantidad_articulos> (cantidad_articulos >= 0)"
        return
    cantidad_articulos = int(sys.argv[1])
    archivo = open(raw_input("Ingrese el nombre del archivo ya parseado: "),"r")
    grafo_wikipedia_es = cargar_articulos(archivo,cantidad_articulos)
    relacionar_articulos(archivo,grafo_wikipedia_es,cantidad_articulos)
    archivo.close()
    print "Bienvenidos a WikipediaUltraMegaRed"
    print "Escoja una opcion, o -1 para finalizar el programa"
    adyacentes = grafo_wikipedia_es.adyacentes("Argentina")
    print adyacentes
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

        menu[opciones[int(entrada) - 1]]()
            
main()
