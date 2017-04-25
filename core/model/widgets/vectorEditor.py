import os
import sys
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtCore import pyqtProperty
from PyQt5.QtWidgets import QStyledItemDelegate

from model.kinematics import Vector

path = os.path.abspath(os.path.dirname('__file__'))
vectorBase, vectorForm = uic.loadUiType(os.path.join(path,"model/ui/vectorEditor.ui"))


class VectorEditor(vectorBase, vectorForm):

    def __init__(self, parent = None):
        super(vectorBase, self).__init__(parent)
        self.setupUi(self)
        self.show()
        self._vector = Vector()

    def setProperty(self, name, variant):
        print(name)

    @property
    def value(self):
        return Vector(self.uiX.value(), self.uiY.value(), self.uiZ.value())

    def setValue(self, vector):
        self.uiX.setValue(vector.x.value)
        self.uiY.setValue(vector.y.value)
        self.uiZ.setValue(vector.z.value)

        self._vector = vector