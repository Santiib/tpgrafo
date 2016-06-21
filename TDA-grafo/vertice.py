class Vertice(object):
    '''Clase que representa a un vertice de un grafo'''

    def __init__(self, dato):
        '''Crea al vertice. El parametro 'dato' indica el dato que guardara el vertice'''

        self.dato = dato
        self.adyacentes = {}
        self.grado_entrada = 0
        self.grado_salida = 0
