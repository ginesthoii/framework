import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit
from PyQt6.QtCore import Qt
from .metadata_engine import extract_metadata


class PreviewPanel(QWidget):
    """
    Shows basic metadata and info for the selected file.
    Later: PDF thumbnails, image previews, etc.
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

        self.title_label = QLabel("No file selected", self)
        self.title_label.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )

        self.meta_view = QTextEdit(self)
        self.meta_view.setReadOnly(True)
        self.meta_view.setPlaceholderText("Metadata and quick info will appear here.")

        layout.addWidget(self.title_label)
        layout.addWidget(self.meta_view)

    def on_file_selected(self, path: str):
        self.current_path = path
        self.title_label.setText(os.path.basename(path))

        metadata = extract_metadata(path)  # stub for now
        if not metadata:
            self.meta_view.setText("(No metadata extracted yet.)")
        else:
            text_lines = [f"{k}: {v}" for k, v in metadata.items()]
            self.meta_view.setText("\n".join(text_lines))
