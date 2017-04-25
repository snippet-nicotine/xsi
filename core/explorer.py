'''
Created on 28 mars 2017

@author: nico
'''
import sys

from PyQt5 import QtWidgets
from PyQt5.Qt import QTreeView, QAbstractItemView

from model.kinematics import Vector
from model.object_3d import Model, Container
from model.scene_graph_model import SceneGraphModel
from model.widgets.editors import Obj3dEditor, TransformEditor
from model.widgets.vectorEditor import VectorEditor


class Explorer(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''

        root = Container("Root")
        model = root.add(Model("Model"))
        test = model.add(Container("test"))
        cns = model.add(Model("Cns"))

        root2 = root.add(Container("Model 2"))
        leg = root2.add(Container("Leg"))
        bones = Model("Fk")
        leg.add(bones)

        bones.transform.scale.y.constrainer = cns.transform.scale.y
        cns.transform.scale = Vector(2,3,4)

        self.model = SceneGraphModel(root)
        self.view = QTreeView()
        self.view.setDragEnabled(True)
        self.view.setAcceptDrops(True)
        self.view.setDropIndicatorShown(True)
        self.view.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.view.setModel(self.model)

        self.objEditor = Obj3dEditor()
        self.objEditor.setModel(self.model)

        self.transformEditor = TransformEditor()
        self.transformEditor.setModel(self.model)

        self.view.selectionModel().currentChanged.connect(self.setSelection)

        self.view.setStyleSheet("""
        .QTreeView {
            background-color:rgb(61, 63, 65);
            color: #bbb;
            font-size : 12px;
            }
        .QHeaderView::section {
            height: 20px;
            font-size : 12px;
            background-color: rgb(65, 74, 91);
            color: #bbb;
            border: 1px solid rgba(20, 24, 24,0);
        }
        """)

    def setSelection(self, current, old):
        self.objEditor.setSelection(current,old)
        self.transformEditor.setSelection(current,old)


    def show(self):
        self.view.show()

 
if __name__ == "__main__":
    
    app = QtWidgets.QApplication(sys.argv)
    explorer = Explorer()
    explorer.show()
    sys.exit(app.exec_())