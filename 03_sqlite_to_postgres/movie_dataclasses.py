import uuid
from dataclasses import dataclass, field


@dataclass
class Filmwork:
    title: str
    description: str
    creation_date: str
    file_path: str
    type: str
    rating: float = field(default=0.0)
    id: uuid.UUID = field(default_factory=uuid.uuid4)

@dataclass
class Genre:
    name: str
    description: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)

@dataclass
class Person:
    full_name: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)

@dataclass
class Genre_film_work:
    film_work_id: uuid.UUID = field(default_factory=uuid.uuid4)
    genre_id: uuid.UUID = field(default_factory=uuid.uuid4)
    id: uuid.UUID = field(default_factory=uuid.uuid4)

@dataclass
class Person_film_work:
    role: str
    film_work_id: uuid.UUID = field(default_factory=uuid.uuid4)
    person_id: uuid.UUID = field(default_factory=uuid.uuid4)
    id: uuid.UUID = field(default_factory=uuid.uuid4)

