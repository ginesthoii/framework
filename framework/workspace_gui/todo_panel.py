from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QLineEdit, QListWidget, QPushButton, QHBoxLayout
)
from PyQt6.QtCore import Qt


class TodoPanel(QWidget):
    """
    Simple local to-do list for workspace tasks.
    Later: persist to JSON.
    """

    def __init__(self, settings_manager, parent=None):
        super().__init__(parent)
        self.settings_manager = settings_manager

        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        title = QLabel("To-Do", self)
        title.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )

        self.list_widget = QListWidget(self)

        input_layout = QHBoxLayout()
        self.input_line = QLineEdit(self)
        self.input_line.setPlaceholderText("New task…")
        btn_add = QPushButton("Add", self)
        btn_add.clicked.connect(self.add_task)
        input_layout.addWidget(self.input_line)
        input_layout.addWidget(btn_add)

        layout.addWidget(title)
        layout.addWidget(self.list_widget, 1)
        layout.addLayout(input_layout)

    def add_task(self):
        text = self.input_line.text().strip()
        if not text:
            return
        self.list_widget.addItem(text)
        self.input_line.clear()
