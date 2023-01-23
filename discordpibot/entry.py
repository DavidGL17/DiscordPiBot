# Define an entry dataclass, wich is sorted and identified by the id

from dataclasses import dataclass
from dataclasses import fields
import json


@dataclass(order=True)
class Entry:
    title: str
    link: str
    id: str

class EntryEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Entry):
            return obj.__dict__
        return super().default(obj)

field_names = [field.name for field in fields(Entry)]

def entryFromFeedparserEntry(entry) -> Entry:
    return Entry(entry.title, entry.link, entry.id)