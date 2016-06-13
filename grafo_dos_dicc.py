from collections import namedtuple

'''Crea un grafo vacio.'''
def grafo_crear():
	grafo_t = namedtuple('grafo', 'vertices relacionados')
	grafo = grafo_t(vertices = {}, relacionados = {})
	return grafo
	
'''Agrega un elemento al grafo sin aristas.'''
def grafo_agregar_vertice(grafo, vertice, dato):
	grafo.vertices[vertice] = dato
	grafo.relacionados[vertice] = []

'''Agrega una arista dirigida del vertice1 al vertice2.'''
def grafo_agregar_arista(grafo, vertice_1, vertice_2):
	if vertice_1 not in grafo.vertices:
		return False
	(grafo.relacionados[vertice_1]).append(vertice_2)
	return True
	
'''Verifica si existe una arista desde el vertice1 dirigida al vertice2.'''
def existe_arista(grafo, vertice_1, vertice_2):
	if (vertice_1 not in grafo.vertices) or (vertice_2 not in (grafo.relacionados[vertice_1])):
		return False
	return True
	
'''Verifica si el grafo esta vacio.'''
def grafo_esta_vacio(grafo):
	if len(grafo.vertices) == 0:
		return True
	return False
	
'''Devuelve el peso de la arista del nodo1 al nodo2.'''
'''def arista_peso(grafo, nodo_1, nodo_2):'''

'''Borra la arista del vertice_1 al vertice_2.'''
def borrar_arista(grafo, nodo_1, vertice_2):
	if (vertice_1 not in grafo.vertices) or (vertice_2 not in grafo.relacionados[vertice_1]):
		return False
	(grafo.relacionados[vertice_1]).pop(vertice_2)
	return True
	
'''Borra vertice del grafo.'''
def borrar_vertice(grafo, vertice):
	if vertice not in grafo.vertices:
		return False
	del grafo.vertices[vertice]
	del grafo.relacionados[vertice]
	return True
	
'''Destruye el grafo'''
def grafo_destruir(grafo):
	del grafo