import random

class Renewables:
    def solar_power(self, hour):
        if 6 <= hour <= 18:
            return max(0, -((hour - 12) ** 2) / 36 + 1) * 50
        return 0

    def wind_power(self):
        return max(0, 20 + random.uniform(-10, 10))