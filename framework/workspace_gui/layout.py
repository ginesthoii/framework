from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSplitter
from PyQt6.QtCore import Qt

from .file_tree_panel import FileTreePanel
from .preview_panel import PreviewPanel
from .rename_panel import RenamePanel
from .todo_panel import TodoPanel


def create_main_widget(parent, settings_manager):
    """
    Builds the main layout:
      [ FileTree | (Preview + Rename stacked) ]
      [                Todo                  ]
    """

    root = QWidget(parent)
    main_layout = QVBoxLayout(root)
    main_layout.setContentsMargins(5, 5, 5, 5)
    main_layout.setSpacing(5)

    # Top splitter: left (tree) / right (preview+rename)
    top_splitter = QSplitter(Qt.Orientation.Horizontal, root)

    file_tree = FileTreePanel(settings_manager, top_splitter)

    right_container = QWidget(top_splitter)
    right_layout = QVBoxLayout(right_container)
    right_layout.setContentsMargins(0, 0, 0, 0)
    right_layout.setSpacing(5)

    preview_panel = PreviewPanel(settings_manager, right_container)
    rename_panel = RenamePanel(settings_manager, right_container)

    right_layout.addWidget(preview_panel, 2)
    right_layout.addWidget(rename_panel, 1)

    top_splitter.addWidget(file_tree)
    top_splitter.addWidget(right_container)
    top_splitter.setStretchFactor(0, 1)
    top_splitter.setStretchFactor(1, 2)

    # Todo panel at bottom
    todo_panel = TodoPanel(settings_manager, root)

    main_layout.addWidget(top_splitter, 3)
    main_layout.addWidget(todo_panel, 1)

    # wiring: when file selected in tree -> preview + rename update
    file_tree.file_selected.connect(preview_panel.on_file_selected)
    file_tree.file_selected.connect(rename_panel.on_file_selected)

    return root
