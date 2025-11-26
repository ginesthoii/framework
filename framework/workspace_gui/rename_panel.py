import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget,
    QLineEdit, QPushButton, QHBoxLayout, QMessageBox
)
from .rules_engine import generate_name_suggestions


class RenamePanel(QWidget):
    """
    Shows auto-generated rename suggestions and allows manual override.
    """

    def __init__(self, settings_manager, parent=None):
        super().__init__(parent)
        self.settings_manager = settings_manager
        self.current_path = None

        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        self.label = QLabel("Rename Suggestions", self)

        self.suggestions_list = QListWidget(self)
        self.suggestions_list.itemClicked.connect(self.on_suggestion_clicked)

        self.manual_input = QLineEdit(self)
        self.manual_input.setPlaceholderText("Manual filename (no path, just name.ext)")

        buttons_layout = QHBoxLayout()
        self.btn_apply = QPushButton("Apply Rename", self)
        self.btn_apply.clicked.connect(self.apply_rename)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.btn_apply)

        layout.addWidget(self.label)
        layout.addWidget(self.suggestions_list, 2)
        layout.addWidget(QLabel("Manual override:", self))
        layout.addWidget(self.manual_input)
        layout.addLayout(buttons_layout)

    def on_file_selected(self, path: str):
        self.current_path = path
        self.suggestions_list.clear()
        self.manual_input.clear()

        if not path:
            return

        suggestions = generate_name_suggestions(path, self.settings_manager)
        for s in suggestions:
            self.suggestions_list.addItem(s)

        if suggestions:
            self.manual_input.setText(suggestions[0])

    def on_suggestion_clicked(self, item):
        self.manual_input.setText(item.text())

    def apply_rename(self):
        if not self.current_path:
            return

        new_name = self.manual_input.text().strip()
        if not new_name:
            QMessageBox.warning(self, "Invalid Name", "Please enter a filename.")
            return

        old_dir = os.path.dirname(self.current_path)
        new_path = os.path.join(old_dir, new_name)

        if os.path.exists(new_path):
            QMessageBox.warning(self, "Conflict", "A file with that name already exists.")
            return

        try:
            os.rename(self.current_path, new_path)
            QMessageBox.information(self, "Renamed", f"Renamed to:\n{new_name}")
            self.current_path = new_path
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to rename file:\n{e}")
