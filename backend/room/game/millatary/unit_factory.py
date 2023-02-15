from units_type import Army, Navy

class CarFactory():
    
    units_function_dict = {
        'army': Army,
        'navy': Navy
    }


    @staticmethod
    def build_car(plan):
        try:
            if plan == "Sedan":
                pass
            raise AssertionError("Unit type is not valid.")


        except AssertionError as e:
            print(e)