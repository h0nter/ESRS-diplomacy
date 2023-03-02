from units import Army, Fleet

class UnitFactory:

    @staticmethod
    def build_unit(plan):
        try:
            if plan == "army":
                return Army()
            elif plan == "fleet":
                return Fleet()
            raise AssertionError("Unit is not valid.")

        except AssertionError as e:
            print(e)