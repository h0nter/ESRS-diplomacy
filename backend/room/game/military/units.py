from abstract_unit import Abstract_unit

class Tank(Abstract_unit):
    def __init__(self) -> None:
        super().__init__()
        self.can_float = False

    def move(self):
        return super().move()

    def support(self):
        return super().support()

    def attend(self):
        return super().attend()


class Warship(Abstract_unit):
    def __init__(self) -> None:
        super().__init__()
        self.can_float = True

    def move(self):
        return super().move()

    def support(self):
        return super().support()

    def attend(self):
        return super().attend()
