from dataclasses import dataclass
import json



@dataclass
class ProcessLink:
    link: str
    status:str
    active:bool

    @classmethod
    def from_data(cls, data:str) -> "ProcessLink":
        return cls(
            link= data,
            status= "new",
            active= True
        )

    def from_json(self) -> str:
        return json.dumps(
            {
                self.link:{
                    "status": self.status,
                    "active": self.active,
                }
            }
        )
    def to_dict(self) -> dict:
        return {
                self.link:{
                    "status": self.status,
                    "active": self.active,
                }
            }
    @classmethod
    def from_dict(cls, data:dict) -> "ProcessLink":
        if len(data) != 1:
            raise ValueError("Invalid Process Link Data format")

        (link, info), = data.items()

        return cls(
            link= str(link),
            status=info.get("status", "new"),
            active=info.get("active", True),
        )
