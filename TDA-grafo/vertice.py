class Vertice(object):
    '''Clase que representa a un vertice de un grafo'''

    def __init__(self, dato):
        '''Crea al vertice. El parametro 'dato' indica el dato que guardara el vertice'''

        self.dato = dato
        self.adyacentes = {}
        self.incidentes = {} #solo interesa si el grafo es dirigido

    def grado_adyacencia(self):
        '''Devuelve la cantidad de aristas que salen del vertice'''

        return len(self.adyacentes)

    def grado_incidencia(self, grafo_es_dirigido):
        
        if grafo_es_dirigido:

            return len(self.incidentes)

        return len(self.adyacentes)

    def obtener_dato(self):

        return self.dato

    def actualizar_dato(self, dato_nuevo):

        self.dato = dato_nuevo
        
    def eliminar_incidencia(self, vertice, grafo_es_dirigido):

        if not grafo_es_dirigido:
        
            raise ValueError

        self.incidentes.pop(vertice)

    def eliminar_adyacencia(self, hasta):

        self.adyacentes.pop(hasta)

    def agregar_adyacencia(self, hasta, peso):

        self.adyacentes[hasta] = peso
    
    def agregar_incidencia(self, desde, peso):

        self.incidentes[desde] = peso

    def es_adyacente(self, vertice):

        return vertice in self.adyacentes

    def obtener_costo_arista(self, hasta):

        return self.adyacentes.get(hasta)

    def obtener_vertices_adyacentes(self):
        
        return [adyacente for adyacente in self.adyacentes]
    
    def obtener_vertices_incidentes(self):
       
        return [incidente for incidente in self.incidentes]
