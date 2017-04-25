'''
Created on 28 mars 2017

@author: nico
'''
from PyQt5.Qt import QAbstractItemModel, QModelIndex


class TreeNode(object):
    
    def __init__(self, parent, row):
        self.parent = parent
        self.row = row
        self.children = self._getChildren()
        
    def _getChildren(self):
        raise NotImplementedError
        
    
class TreeModel(QAbstractItemModel):
    
    def __init__(self):
        QAbstractItemModel.__init__(self)
        self.rootNodes = self._getRootNodes()
    
    def _getRootNodes(self):
        raise NotImplementedError
    
    def index(self, row, column, parent):
        if not parent.isValid() and len(self.rootNodes) > row:
            return self.createIndex(row, column, self.rootNodes[row])
        parentNode = parent.internalPointer()
        return self.createIndex(row, column, parentNode.children[row])
    
    def parent(self, index):
        if not index.isValid():
            return QModelIndex()
        node = index.internalPointer()
        
        if node.parent is None:
            return QModelIndex()
        else:
            return self.createIndex(node.parent.row, 0 , node.parent)
        
    def reset(self):
        self.rootNodes = self._getRootNodes()
    
    def rowCount(self, parent):
        if not parent.isValid():
            return len(self.rootNodes)
        
        node = parent.internalPointer()
        return len(node.children)