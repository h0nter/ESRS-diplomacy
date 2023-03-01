from abstract_unit import AbstractUnit

class Army(AbstractUnit):
    def __init__(self) -> None:
        super().__init__()
        self.can_float = False

    def move(self):
        return super().move()

    def support(self):
        return super().support()


class Fleet(AbstractUnit):
    def __init__(self) -> None:
        super().__init__()
        self.can_float = True

    def move(self):
        return super().move()

    def support(self):
        return super().support()

    def convoy(self):
        return super().attend()