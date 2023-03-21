from .units import Army, Fleet


class UnitFactory:
    # input with a order object
    @staticmethod
    def build_unit(order:classmethod) -> object:
        try:
            if order.target_unit.can_float: 
                return Fleet(order)
            else:
                return Army(order)
        except AssertionError as e:
            print(e)

    @classmethod
    def batch_build(cls, orders_list:list) -> list:
        militaries = list()
        for order in orders_list:
            militaries.append(cls.build_unit(order))
        return militaries
