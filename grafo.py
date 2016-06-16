from cola import *

visitar_nulo = lambda a,b,c,d: True
heuristica_nula = lambda actual,destino: 0

ADYACENCIAS = 1
DATO_VERTICE = 0

def _dfs(grafo, actual, visitados, orden, padre, visitar, extra):

    continuar = visitar(actual, padre, orden, extra)

    if not continuar:
        return 

    visitados.append(actual)
    adyacentes = grafo.adyacentes(actual)

    for vertice in adyacentes:

        if vertice not in visitados :

            padre[vertice] = actual
            orden[vertice] = orden[actual] + 1
            _dfs(grafo, vertice, visitados, orden, padre, visitar, extra)


def _bfs(grafo, origen, visitados, orden, padre, visitar, extra):  

    cola = Cola()
    cola.encolar(origen)
    visitados.append(origen)
        
    while not cola.esta_vacia():
            
        actual = cola.desencolar()
        continuar = visitar(actual, padre, orden, extra)

        if not continuar:

           return 

        adyacentes = grafo.adyacentes(actual)

        for vertice in adyacentes:

            if vertice not in visitados:

                visitados.append(vertice)
                padre[vertice] = actual
                orden[vertice] = orden[actual] + 1       
                cola.encolar(vertice)


def recorrido(grafo, tipo_recorrido, inicio, visitar, extra):

        visitados = []
        padre = dict()
        orden = dict()
        
        if not inicio:
            for vertice in grafo:
                if vertice not in visitados:
                    padre[vertice] = None
                    orden[vertice] = 0
                    tipo_recorrido(grafo, vertice, visitados, orden, padre, visitar, extra)
        else:

            padre[inicio] = None 
            orden[inicio] = 0

            tipo_recorrido(grafo, inicio, visitados, orden, padre, visitar, extra)
        return padre,orden

def obtener_componentes_conexas(vertice,padre,orden,lista_componentes):

    if not padre[vertice]:
        lista_componentes.append([vertice])

    else:
        ultima_componente = len(lista_componentes) - 1
        lista_componentes[ultima_componente].append(vertice)    

    return True        

class Grafo(object):
    '''Clase que representa un grafo. El grafo puede ser dirigido, o no, y puede no indicarsele peso a las aristas
    (se comportara como peso = 1). Implementado como "diccionario de diccionarios"'''
    
    def __init__(self, es_dirigido = False):
        '''Crea el grafo. El parametro 'es_dirigido' indica si sera dirigido, o no.'''

        self.dirigido = es_dirigido
        self.cantidad_vertices = 0
        self.vertices = {} #contiene a los vertices y a sus adyacentes
            
    def __len__(self):
        '''Devuelve la cantidad de vertices del grafo'''

        return self.cantidad_vertices
    
    def __iter__(self):
        '''Devuelve un iterador de vertices, sin ningun tipo de relacion entre los consecutivos'''

        for k in self.vertices:

            yield k
        
    def keys(self):
        '''Devuelve una lista de identificadores de vertices. Iterar sobre ellos es equivalente a iterar sobre el grafo.'''

        return [k for k in self.vertices]

    def __getitem__(self, id):
        '''Devuelve el valor del vertice asociado, del identificador indicado. Si no existe el identificador en el grafo, lanzara KeyError.'''
        
        return self.vertices[id][DATO_VERTICE]
    
    def __setitem__(self, id, valor):
        '''Agrega un nuevo vertice con el par <id, valor> indicado. ID debe ser de identificador unico del vertice.
        En caso que el identificador ya se encuentre asociado a un vertice, se actualizara el valor.
        '''

        if id in self.vertices:

            self.vertices[id][DATO_VERTICE] = valor

        else:

            self.vertices[id] = [valor,dict()]
            self.cantidad_vertices+=1
    
    def __delitem__(self, id):
        '''Elimina el vertice del grafo, y devuelve el valor asociado. Si no existe el identificador en el grafo, lanzara KeyError.
        Borra tambien todas las aristas que salian y entraban al vertice en cuestion.
        '''
        dato = self.vertices[id][DATO_VERTICE]  
      
        for k in self.vertices[id][ADYACENCIAS]:

            self._borrar_arista(k,id,1) 

        self.vertices.pop(id)
        self.cantidad_vertices-=1
        return dato
        
    def __contains__(self, id):
        ''' Determina si el grafo contiene un vertice con el identificador indicado.'''

        return id in self.vertices

    def _agregar_arista(self, desde, hasta, peso, recursion):
        
        if recursion > 1:

            return

        nueva_arista = (desde,hasta)                
        self.vertices[desde][ADYACENCIAS][hasta] = peso

        if not self.dirigido:

            self._agregar_arista(hasta,desde,peso,recursion+1)

    def agregar_arista(self, desde, hasta, peso = 1):
        '''Agrega una arista que conecta los vertices indicados. Parametros:
            - desde y hasta: identificadores de vertices dentro del grafo. Si alguno de estos no existe dentro del grafo, lanzara KeyError.
            - Peso: valor de peso que toma la conexion. Si no se indica, valdra 1.
            Si el grafo es no-dirigido, tambien agregara la arista reciproca.
        '''
        self._agregar_arista(desde, hasta, peso, 0)
        
    def _borrar_arista(self,desde,hasta,paso_recursivo):

        if paso_recursivo > 1 or (paso_recursivo == 1 and desde == hasta): #En el caso de que este en un grafo no dirigido, o con un lazo
            return

        if self.vertices[hasta] and self.vertices[desde]:

            try:
               
               self.vertices[desde][ADYACENCIAS].pop(hasta)
            except KeyError:

                raise ValueError

        if not self.dirigido:

            self._borrar_arista(hasta,desde,paso_recursivo+1)      
                
    def borrar_arista(self, desde, hasta):
        '''Borra una arista que conecta los vertices indicados. Parametros:
            - desde y hasta: identificadores de vertices dentro del grafo. Si alguno de estos no existe dentro del grafo, lanzara KeyError.
           En caso de no existir la arista, se lanzara ValueError.
        '''
        recursion = 0
        self._borrar_arista(desde,hasta,recursion)

    def obtener_peso_arista(self, desde, hasta):
        '''Obtiene el peso de la arista que va desde el vertice 'desde', hasta el vertice 'hasta'. Parametros:
            - desde y hasta: identificadores de vertices dentro del grafo. Si alguno de estos no existe dentro del grafo, lanzara KeyError.
            En caso de no existir la union consultada, se devuelve None.
        '''
        if self.vertices[hasta] and self.vertices[desde]:

            return self.vertices[desde][ADYACENCIAS].get(hasta)
       
    def adyacentes(self, id):
        '''Devuelve una lista con los vertices (identificadores) adyacentes al indicado. Si no existe el vertice, se lanzara KeyError'''
        return [k for k in self.vertices[id][ADYACENCIAS]]

 
    def bfs(self, inicio=None, visitar = visitar_nulo, extra = None):
        '''Realiza un recorrido BFS dentro del grafo, aplicando la funcion pasada por parametro en cada vertice visitado.
        Parametros:
            - visitar: una funcion cuya firma sea del tipo: 
                    visitar(v, padre, orden, extra) -> Boolean
                    Donde 'v' es el identificador del vertice actual, 
                    'padre' el diccionario de padres actualizado hasta el momento,
                    'orden' el diccionario de ordenes del recorrido actualizado hasta el momento, y 
                    'extra' un parametro extra que puede utilizar la funcion (cualquier elemento adicional que pueda servirle a la funcion a aplicar). 
                    La funcion aplicar devuelve True si se quiere continuar iterando, False en caso contrario.
            - extra: el parametro extra que se le pasara a la funcion 'visitar'
            - inicio: identificador del vertice que se usa como inicio. Si se indica un vertice, el recorrido se comenzara en dicho vertice, 
            y solo se seguira hasta donde se pueda (no se seguira con los vertices que falten visitar)
        Salida:
            Tupla (padre, orden), donde :
                - 'padre' es un diccionario que indica para un identificador, cual es el identificador del vertice padre en el recorrido BFS (None si es el inicio)
                - 'orden' es un diccionario que indica para un identificador, cual es su orden en el recorrido BFS
        '''
        padre,orden = recorrido(self, _bfs, inicio, visitar, extra)   
        return padre,orden
        

    def dfs(self, inicio=None, visitar = visitar_nulo, extra = None):
        '''Realiza un recorrido DFS dentro del grafo, aplicando la funcion pasada por parametro en cada vertice visitado.
        - visitar: una funcion cuya firma sea del tipo: 
                    visitar(v, padre, orden, extra) -> Boolean
                    Donde 'v' es el identificador del vertice actual, 
                    'padre' el diccionario de padres actualizado hasta el momento,
                    'orden' el diccionario de ordenes del recorrido actualizado hasta el momento, y 
                    'extra' un parametro extra que puede utilizar la funcion (cualquier elemento adicional que pueda servirle a la funcion a aplicar). 
                    La funcion aplicar devuelve True si se quiere continuar iterando, False en caso contrario.
            - extra: el parametro extra que se le pasara a la funcion 'visitar'
            - inicio: identificador del vertice que se usa como inicio. Si se indica un vertice, el recorrido se comenzara en dicho vertice, 
            y solo se seguira hasta donde se pueda (no se seguira con los vertices que falten visitar)
        Salida:
            Tupla (padre, orden), donde :
                - 'padre' es un diccionario que indica para un identificador, cual es el identificador del vertice padre en el recorrido DFS (None si es el inicio)
                - 'orden' es un diccionario que indica para un identificador, cual es su orden en el recorrido DFS
        '''
        padre,orden = recorrido(self, _dfs, inicio, visitar, extra)   
        return padre,orden
        
    
    def componentes_conexas(self):
        '''Devuelve una lista de listas con componentes conexas. Cada componente conexa es representada con una lista, con los identificadores de sus vertices.
        Solamente tiene sentido de aplicar en grafos no dirigidos, por lo que
        en caso de aplicarse a un grafo dirigido se lanzara TypeError'''

        if self.dirigido:
            raise TypeError 

        lista_componentes_conexas = []
        self.bfs(None, obtener_componentes_conexas,lista_componentes_conexas)

        return lista_componentes_conexas

    def camino_minimo(self, origen, destino, heuristica=heuristica_nula):
        '''Devuelve el recorrido minimo desde el origen hasta el destino, aplicando el algoritmo de Dijkstra, o bien
        A* en caso que la heuristica no sea nula. Parametros:
            - origen y destino: identificadores de vertices dentro del grafo. Si alguno de estos no existe dentro del grafo, lanzara KeyError.
            - heuristica: funcion que recibe dos parametros (un vertice y el destino) y nos devuelve la 'distancia' a tener en cuenta para ajustar los resultados y converger mas rapido.
            Por defecto, la funcion nula (devuelve 0 siempre)
        Devuelve:
            - Listado de vertices (identificadores) ordenado con el recorrido, incluyendo a los vertices de origen y destino. 
            En caso que no exista camino entre el origen y el destino, se devuelve None. 
        '''
        raise NotImplementedError()
    
    def mst(self):
        '''Calcula el Arbol de Tendido Minimo (MST) para un grafo no dirigido. En caso de ser dirigido, lanza una excepcion.
        Devuelve: un nuevo grafo, con los mismos vertices que el original, pero en forma de MST.'''
        raise NotImplementedError()
