from configparser import ConfigParser
from pathlib import Path

class ConfigManager:
    _instance = None
    _config = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._initialize_config()
        return cls._instance

    @classmethod
    def _initialize_config(cls):
        config_path = Path(__file__).parent.parent.joinpath('config', 'config.ini')
        cls._config = ConfigParser()
        cls._config.read(config_path)

    @property
    def config(self):
        return self._config

app_config = ConfigManager()