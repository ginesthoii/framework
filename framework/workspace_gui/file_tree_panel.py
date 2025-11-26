import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTreeView, QFileSystemModel, QFileDialog, QLabel
)
from PyQt6.QtCore import pyqtSignal, QModelIndex


class FileTreePanel(QWidget):
    """
    Left panel:
      - Folder chooser button
      - File system tree view
    Emits: file_selected(path: str)
    """
    file_selected = pyqtSignal(str)

    def __init__(self, settings_manager, parent=None):
        super().__init__(parent)
        self.settings_manager = settings_manager

        self.model = QFileSystemModel(self)
        self.model.setRootPath(os.path.expanduser("~"))
        self.model.setReadOnly(True)

        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        top_bar = QHBoxLayout()
        self.current_root_label = QLabel("Root: ~", self)
        btn_choose_root = QPushButton("Choose Folder", self)
        btn_choose_root.clicked.connect(self.choose_root)

        top_bar.addWidget(self.current_root_label)
        top_bar.addStretch()
        top_bar.addWidget(btn_choose_root)

        self.tree = QTreeView(self)
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(os.path.expanduser("~")))
        self.tree.doubleClicked.connect(self.on_item_double_clicked)
        self.tree.setHeaderHidden(True)

        layout.addLayout(top_bar)
        layout.addWidget(self.tree)

    def choose_root(self):
        folder = QFileDialog.getExistingDirectory(
            self, "Select Root Folder", os.path.expanduser("~")
        )
        if folder:
            self.model.setRootPath(folder)
            self.tree.setRootIndex(self.model.index(folder))
            self.current_root_label.setText(f"Root: {folder}")

    def on_item_double_clicked(self, index: QModelIndex):
        if not index.isValid():
            return
        path = self.model.filePath(index)
        if os.path.isfile(path):
            self.file_selected.emit(path)
