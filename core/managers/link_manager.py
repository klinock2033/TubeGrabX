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




    def update_status(self, link: str, status: str) -> bool:

        status = self.normalize_text(status)
        link = self.normalize_text(link)

        valid_status = {
            'new',
            'error',
            'processing',
            'finished',
            'retried',
        }

        if status not in valid_status:
            raise Exception(f"Invalid status: {status}")

        for pl in self.links:
            if pl.link == link:
                pl.status = status
                self.save()
                return True

        return False

    def remove_link(self, link: str):
        for pl in self.links:
            if pl.link == link:
                self.links.remove(pl)
                self.save()
                return True

        return False


    def set_link_active(self, link: str, value:bool):
        if not isinstance(value, bool):
            raise Exception(f"Invalid data type, can't activate link")

        link = self.normalize_text(link)

        if link == "*":
            for pl in self.links:
                pl.active = value

        if link != "*" and link != "":
            for pl in self.links:
                if pl.link == link:
                    pl.active = value
        self.save()

    def get_active_links(self):
        active_links = []
        for pl in self.links:
            if pl.active:
                active_links.append(pl)
        return active_links

    @staticmethod
    def normalize_text(text: str):
        if not isinstance(text, str):
            raise Exception(f"Invalid data type, can't normalize text")
        text = text.strip()
        text = text.lower()
        return text

