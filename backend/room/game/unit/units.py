from .abstract_unit import AbstractUnit


class Army(AbstractUnit):
    def __init__(self, order) -> None:
        super().__init__(order)
    
    def move(self):
        super().move()

    def support(self):
        super().support()


class Fleet(AbstractUnit):
    def __init__(self, order) -> None:
        super().__init__(order)

    def move(self):
        super().move()

    def support(self):
        super().support()

    def convoy(self):
        pass
