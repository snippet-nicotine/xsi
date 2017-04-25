from PyQt5 import QtWidgets

class PanelObj3D(QtWidgets.QDataWidgetWrapper):

    def __init__(self, parent = None):
        super(PanelObj3D, self).__init__(parent)

        self.nameField = QtWidgets.QLabel()
        self.parentField = QtWidgets.QLabel()

        self.addMapping(self.nameField, 0)
        self.addMapping(self.parentField, 1)