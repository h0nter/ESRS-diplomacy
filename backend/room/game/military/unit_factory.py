from units import Tank, Warship

class UnitFactory:

    @staticmethod
    def build_unit(plan):
        try:
            if plan == "army":
                return Tank()
            elif plan == "navy":
                return Warship()
            raise AssertionError("Unit is not valid.")

        except AssertionError as e:
            print(e)