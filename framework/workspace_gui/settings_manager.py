import json
import os

DEFAULT_SETTINGS = {
    "naming_style": "snake_case",
    "include_date": True,
    "date_format": "YYYY-MM-DD",
    "include_project_name": True,
    "include_version": True,
    "include_category": True,
    "order": ["date", "project_name", "category", "version", "title"],
    "default_preset": "developer_standard"
}


class SettingsManager:
    """
    Handles reading/writing settings and naming presets from JSON files.
    """

    def __init__(self, config_dir=None):
        if config_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            config_dir = os.path.join(base_dir, "config")

        self.config_dir = config_dir
        self.settings_path = os.path.join(config_dir, "settings.json")
        self.presets_path = os.path.join(config_dir, "naming_presets.json")

        self.settings = self._load_settings()
        self.presets = self._load_presets()

    def _load_settings(self):
        if not os.path.exists(self.settings_path):
            os.makedirs(self.config_dir, exist_ok=True)
            with open(self.settings_path, "w", encoding="utf-8") as f:
                json.dump(DEFAULT_SETTINGS, f, indent=2)
            return DEFAULT_SETTINGS.copy()

        with open(self.settings_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        merged = DEFAULT_SETTINGS.copy()
        merged.update(data)
        return merged

    def _load_presets(self):
        if not os.path.exists(self.presets_path):
            default_presets = {
                "developer_standard": "{date}_{project}_{title}_{version}",
                "minimal": "{title}",
                "research": "{author}_{year}_{title}",
                "media": "{date}_{category}_{title}"
            }
            with open(self.presets_path, "w", encoding="utf-8") as f:
                json.dump(default_presets, f, indent=2)
            return default_presets

        with open(self.presets_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_setting(self, key, default=None):
        return self.settings.get(key, default)

    def get_preset(self, name):
        return self.presets.get(name)
