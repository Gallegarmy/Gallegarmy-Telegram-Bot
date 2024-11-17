import random
from dataclasses import dataclass
from typing import Text, Optional


@dataclass(frozen=True)
class Admin:
    name: Text
    username: Text

    def username_as_handle(self) -> Text:
        return f"@{self.username}"


class InMemoryAdministratorsStorage:

    def __init__(self):
        self.administrators: Dict[Text, Admin] = {
            'Qrow01': Admin('Nacho', 'Qrow01'),
            'juanprm': Admin('Juan', 'juanprm'),
            'Yisus1982': Admin('Yisus', 'Yisus1982'),
            'madtyn': Admin('Martin', 'madtyn'),
            'soulcodex': Admin('Roberto', 'soulcodex'),
        }

    def exists_by_handle(self, handle: Text) -> bool:
        if handle in self.administrators:
            return True

        return False

    def search_by_handle(self, handle: Text) -> Optional[Admin]:
        if handle in self.administrators:
            return self.administrators[handle]

        return None

    def fetch_one_randomly(self) -> Admin:
        idx = random.randint(0, len(self.administrators) - 1)
        key = list(self.administrators.keys())[idx]
        return self.administrators[key]
