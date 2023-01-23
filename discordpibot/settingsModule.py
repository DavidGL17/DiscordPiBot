import yaml

# Settings


class Settings:
    def __init__(self):
        self._settings = self._load_settings()

    def _load_settings(self):
        with open("settings.yaml", "r") as f:
            return yaml.safe_load(f)
