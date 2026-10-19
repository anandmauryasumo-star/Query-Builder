import os

from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

from .query_builder_dialog import QueryBuilderDialog


class QueryBuilder:

    def __init__(self, iface):
        self.iface = iface
        self.action = None

    def initGui(self):

        icon_path = os.path.join(
            os.path.dirname(__file__),
            "icon.png"
        )

        self.action = QAction(
            QIcon(icon_path),
            "Query Builder",
            self.iface.mainWindow()
        )

        self.action.triggered.connect(self.run)

        self.iface.addPluginToMenu(
            "&Query Builder",
            self.action
        )

        self.iface.addToolBarIcon(
            self.action
        )

    def unload(self):

        if self.action:
            self.iface.removePluginMenu(
                "&Query Builder",
                self.action
            )

            self.iface.removeToolBarIcon(
                self.action
            )

    def run(self):

        dlg = QueryBuilderDialog(
            self.iface
        )

        dlg.exec_()
