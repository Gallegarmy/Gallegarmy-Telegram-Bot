from faker import Faker


class FakerFactory:

    def __init__(self):
        self.faker: Optional[Faker] = None

    def new_faker(self):
        if self.faker is None:
            self.faker = Faker()

        return self.faker
