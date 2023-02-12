from abstract_unit import Abstract_unit

class Army(Abstract_unit):
    def __init__(self) -> None:
        super().__init__()

    def move(self):
        return super().move()

    def support(self):
        return super().support()

    def attend(self):
        return super().attend()


class Navy(Abstract_unit):
    def __init__(self) -> None:
        super().__init__()

    def move(self):
        return super().move()

    def support(self):
        return super().support()

    def attend(self):
        return super().attend()
