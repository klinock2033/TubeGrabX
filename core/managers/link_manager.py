from core.config import AppConfig
from core.models.link_model import ProcessLink
import json
from pathlib import Path

class LinkManager:
    def __init__(self, config: AppConfig):
        self.config = config
        self.links: list[ProcessLink] = []

    def add_link(self, link: str):
        if any(l.link == link for l in self.links):
            return None

        pl = ProcessLink.from_data(link)
        self.links.append(pl)
        return pl


    def load(self):
        try:
            with open(self.config.save_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.links = [ProcessLink.from_dict(item) for item in data]

        except FileNotFoundError:
            self.links = []

        except json.decoder.JSONDecodeError:
            self.links = []


    def save(self):
        Path(self.config.save_file).parent.mkdir(parents=True, exist_ok=True)
        try:
            data = [link.to_dict() for link in self.links]
            with open(self.config.save_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)


        except Exception as e:

            raise Exception(f"Failed to save links: {e}")




    def update_status(self, link: str, status: str):
        ...

    def remove_link(self, link: str):
        ...

    def get_active_links(self):
        ...