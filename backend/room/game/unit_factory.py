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

    @staticmethod
    def batch_buils(orders_list:list) -> list:
        militaries = list()
        for order in orders_list:
            militaries.append(UnitFactory.build_unit(order))
        return militaries
