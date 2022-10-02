


class Graph():
    def __init__(self):
        self.matrix = {}
        self.emptyValue = []
        
    def addVertex(self, x, y):
        
        self.matrix[(x,y)] = []
        
        
    def addEdge(self, parentX, parentY, destinationX, destinationY):
        self.matrix[(parentX, parentY)].append((destinationX, destinationY))
        
