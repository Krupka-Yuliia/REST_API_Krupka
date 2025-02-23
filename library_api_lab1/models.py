from dataclasses import dataclass, field
import uuid


@dataclass()
class Book:
    title: str = field(metadata={"required": True})
    author: str = field(metadata={"required": True})
    year: int = field(metadata={"required": True})
    publisher: str = field(metadata={"required": True})
    id: str = field(default_factory=lambda: str(uuid.uuid4()))


books = [
    Book(
        id=str(uuid.uuid4()),
        title="Pride And Prejudice",
        author="Jane Austen",
        year=1812,
        publisher="Vivat",
    ),
    Book(
        id=str(uuid.uuid4()),
        title="Six of Crows",
        author="Leigh Bardugo",
        year=2015,
        publisher="KSD",
    ),
    Book(
        id=str(uuid.uuid4()),
        title="Cruel Prince",
        author="Holly Black",
        year=2018,
        publisher="Vivat",
    )
]
