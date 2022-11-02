# Define an entry dataclass, wich is sorted and identified by the id

from dataclasses import dataclass

@dataclass(order=True)
class Entry:
    title: str
    link: str
    id: str

def entryFromFeedparserEntry(entry) -> Entry:
    return Entry(entry.title, entry.link, entry.id)