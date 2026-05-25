import os
from dataclasses import dataclass

@dataclass
class AppConfig:
    app_name: str
    app_version: str
    save_file: str
    retry_interval: int

    @classmethod
    def from_env(cls)->"AppConfig":
        return cls(
            app_name=os.getenv("APP_NAME", "YouEZ Download"),
            app_version=os.getenv("APP_VERSION", "1.0.0"),
            save_file=os.getenv("APP_SAVE_FILE", "data/save.json"),
            retry_interval=int(os.getenv("APP_RETRY_INTERVAL", "1")),

        )