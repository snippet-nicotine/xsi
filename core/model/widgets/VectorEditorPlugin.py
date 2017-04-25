from PyQt5.QtDesigner import QPyDesignerCustomWidgetPlugin

from model.widgets.vectorEditor import VectorEditor


class VectorEditorPlugin(QPyDesignerCustomWidgetPlugin):
    
    def __init__(self, parent=None):
        super(VectorEditorPlugin, self).__init__(parent)
        self.initialized = False

    def initialize(self, formEditor):
        if self.initialized:
            return

        manager = formEditor.extensionManager()
        if manager:
            self.factory = \
                VectorMenuFactory(manager)
            manager.registerExtensions(
                self.factory,
                "com.trolltech.Qt.Designer.TaskMenu")

        self.initialized = True

    def createWidget(self, parent):
        return VectorEditor(parent)

    def name(self):
        return "VectorWidget"

    def includeFile(self):
        return "vectorEditor"