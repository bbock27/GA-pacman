


class Node():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.position = (x,y)
        self.neighbors = []
        
    
    def addNeighbor(self, newX, newY):
        self.neighbors.append((newX, newY))
        
        




































# class Node():
#     def __init__(self, data, isRoot = False, prev = None):
#         self.data = data
#         self.children = []
#         self.isRoot = isRoot
#         self.previous = prev
            
            
#     def addChild(self, child):
#         self.children.append(child)
        
        
        
#     def getData(self):
#         return self.data
    
#     def getChildren(self):
#         return self.children
    
#     def getIsRoot(self):
#         return self.isRoot
    
#     def getPrevious(self):
#         return self.previous
    
    
    
#     def setData(self, newData):
#         self.data = newData
    
#     def setIsRoot(self, isRoot):
#         self.isRoot = isRoot
    
#     def setPrevious(self, newPrevious):
#         self.previous = newPrevious
        
        
        
        
        
#     def addChild(self, newData):
#         newChild = Node(newData, False, self)
#         self.children.append(newChild)
