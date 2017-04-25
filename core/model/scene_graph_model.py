'''
Created on 28 mars 2017

@author: nico
'''
from PyQt5 import QtGui
from PyQt5.Qt import QPixmap

import model.icons_qrc

import PyQt5.QtCore as QtCore
from model.abstract_treemodel import TreeModel, TreeNode
from model.kinematics import Transform


class Node(TreeNode):
    
    def __init__(self, ref, parent, row):
        self.ref = ref
        
        TreeNode.__init__(self, parent, row)
        
    def _getChildren(self):
        return [Node(obj, self, index) for index, obj in enumerate(self.ref.children)]
    
        

class SceneGraphModel(TreeModel):
    '''
    classdocs
    '''

    def __init__(self, root):
        '''
        Constructor
        '''
        
        self.root = root
        self.rootElements = root.children
        
        TreeModel.__init__(self)
    
    def columnCount(self, parent):
        return 3
    
    def data(self, index, role):
        if not index.isValid():
            return None
        
        node = index.internalPointer()
        
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            if index.column() == 0:
                return node.ref.name
                
            if index.column() == 1:
                return node.ref.TYPE
            
            if index.column() == 2:
                try:
                    return node.ref.transform
                except:
                    pass

            if index.column() == 3:
                try:
                    return node.ref.parent.name
                except:
                    pass
        
        if role == QtCore.Qt.DecorationRole:
            if index.column() == 0:
                type = node.ref.TYPE
                
                if type == "Container":
                    return QtGui.QIcon(QPixmap(":/folder"))
                if type == "Model":
                    return QtGui.QIcon(QPixmap(":/color-cube"))
            
            if index.column() == 2:
                try:
                    if node.ref.isConstrained:
                        return QtGui.QIcon(QPixmap(":/link"))
                except:
                    pass
                
            
        return None
    
    def setData(self, index, value, role = QtCore.Qt.EditRole):
        if index.isValid():
        
            if role == QtCore.Qt.EditRole:
                if index.column() == 0:
                    node = index.internalPointer()
                    node.ref.name = value

                if index.column() == 2:
                    node = index.internalPointer()
                    node.ref.transform = value

                self.dataChanged.emit(index, index)
                return True

        return False
        
    
    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole  and section == 0:
            return "Name"
        return None 
    
    def supportedDropActions(self):
        return QtCore.Qt.MoveAction | QtCore.Qt.CopyAction
    
    def flags(self, index):
        if index.column() == 0 or index.column() == 2:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled
        else:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDropEnabled
    
    def mimeTypes(self):
        return [ "application/x-tech.artists.org" ]
    
    def mimeData(self, indices):

        mimeData      = QtCore.QMimeData()
        encodedData = QtCore.QByteArray()
        stream         = QtCore.QDataStream(encodedData, QtCore.QIODevice.WriteOnly)

        for index in indices:
            if not index.isValid():
                continue
            node = index.internalPointer()
                
            variant = QtCore.QVariant(node)
                
            # add all the items into the stream
            stream << variant
                
        print("Encoding drag with: ", "application/x-tech.artists.org")
        mimeData.setData("application/x-tech.artists.org", encodedData)
        return mimeData
    
    def dropMimeData(self, data, action, row, column, parent):

        if action == QtCore.Qt.CopyAction:
            print("Copying")
        elif action == QtCore.Qt.MoveAction:
            print("Moving")
        print("Param data:", data)
        print("Param row:",  row)
        print("Param column:", column)
        print("Param parent:", parent)

        # Where are we inserting?
        beginRow = 0
        if row != -1:
            print("ROW IS NOT -1, meaning inserting inbetween, above or below an existing node")
            beginRow = row
        elif parent.isValid():
            print("PARENT IS VALID, inserting ONTO something since row was not -1, beginRow becomes 0 because we want to insert it at the begining of this parents children")
            beginRow = 0
        else:
            print("PARENT IS INVALID, inserting to root, can change to 0 if you want it to appear at the top")
            beginRow = self.rowCount(QtCore.QModelIndex())

        # create a read only stream to read back packed data from our QMimeData
        encodedData = data.data("application/x-tech.artists.org")

        stream = QtCore.QDataStream(encodedData, QtCore.QIODevice.ReadOnly)


        # decode all our data back into dropList
        dropList = []
        numDrop = 0

        while not stream.atEnd():
            variant = QtCore.QVariant()
            stream >> variant # extract
            node = variant
            
            # add the python object that was wrapped up by a QVariant back in our mimeData method
            dropList.append( node ) 

            # number of items to insert later
            numDrop += 1


        print ("INSERTING AT", beginRow, "WITH", numDrop, "AMOUNT OF ITEMS ON PARENT:", parent.internalPointer())
        
        # This will insert new items, so you have to either update the values after the insertion or write your own method to receive our decoded dropList objects.
        self.insertRows(beginRow, numDrop, parent) 
        
        for drop in dropList:
            # If you don't have your own insertion method and stick with the insertRows above, this is where you would update the values using our dropList.
            pass
    
    def _getRootNodes(self):
        return [Node(obj, None, index) for index, obj in enumerate(self.rootElements) ]