import os
import sys

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QAbstractItemDelegate, QItemDelegate

from model.kinematics import Transform

path = os.path.abspath(os.path.dirname('__file__'))
obj3dBase, obj3dForm = uic.loadUiType(os.path.join(path,"model/ui/obj3dEditor.ui"))
transfoBase, transfoForm = uic.loadUiType(os.path.join(path,"model/ui/TransformEditor.ui"))


class Obj3dEditor(obj3dBase, obj3dForm):

    def __init__(self, parent = None):
        super(obj3dBase, self).__init__(parent)
        self.setupUi(self)
        self.show()
        self._dataWrapper = QtWidgets.QDataWidgetMapper()

    def setModel(self, model):
        self._model = model
        self._dataWrapper.setModel(model)

        self._dataWrapper.addMapping(self.uiName, 0)
        self._dataWrapper.addMapping(self.uiType, 1)
        self._dataWrapper.addMapping(self.uiParent, 3)

    def setSelection(self, current, old):
        parent = current.parent()
        self._dataWrapper.setRootIndex(parent)
        self._dataWrapper.setCurrentModelIndex(current)

class TransformEditor(transfoBase, transfoForm):

    def __init__(self, parent = None):
        super(TransformEditor, self).__init__(parent)
        self.setupUi(self)
        self._dataWrapper = QtWidgets.QDataWidgetMapper()
        self._dataWrapper.setItemDelegate(TransformDelegate())
        self.show()

    def setModel(self, model):
        self._model = model
        self._dataWrapper.setModel(model)
        self._dataWrapper.addMapping(self, 2)

    def setSelection(self, current, old):
        parent = current.parent()
        self._dataWrapper.setRootIndex(parent)
        self._dataWrapper.setCurrentModelIndex(current)

class TransformDelegate(QItemDelegate):
    
    def __init__(self):
        super(TransformDelegate, self).__init__()

    def setEditorData(self, editor, index):
        node = index.internalPointer()
        try:
            editor.uiScale.setValue(node.ref.transform.scale)

        except:
            e = sys.exc_info()[0]
            print("[TransformDelegate] Error: ", e)

    def setModelData(self, editor, model, index):
        print("setModelData")
        vScale = editor.uiScale.value
        vRotation = editor.uiRotation.value
        vPosition = editor.uiPosition.value

        model.setData(index, Transform(vScale, vRotation, vPosition))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    sys.exit(app.exec_())