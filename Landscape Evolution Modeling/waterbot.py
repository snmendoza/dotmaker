


class Waterbot:

    def __init__(self,constants):
        self.constants = constants
        self.sediment = 0

    def erode_or_deposit(self, gradient):
        if gradient > self.sediment*(self.constants.erode_constant):
            erode_amount = self.constants.get_sediment_amount(gradient)
            self.sediment = self.sediment + erode_amount

            return -(self.constants.get_terrain_z_delta(erode_amount))
        else:
            erode_amount = self.constants.get_sediment_amount(gradient)
            self.sediment = self.sediment + erode_amount

            return self.constants.get_terrain_z_delta(erode_amount)
        
