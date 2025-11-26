from PyQt6.QtWidgets import QMainWindow
from .layout import create_main_widget
from .settings_manager import SettingsManager


class MainWindow(QMainWindow):
    """
    Main window for the Framework GUI.
    Holds:
      - left: file tree / inventory
      - right: preview + rename suggestions
      - bottom: to-do list
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("FrameworkOS – Workspace")
        self.resize(1200, 800)

        # Settings manager (loads config/settings.json)
        self.settings_manager = SettingsManager()

        # Central layout widget
        self.central = create_main_widget(self, self.settings_manager)
        self.setCentralWidget(self.central)

        self._init_status_bar()

    def _init_status_bar(self):
        self.statusBar().showMessage("Ready")
