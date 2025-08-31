class Pricing:
    def __init__(self, base_price=0.15):
        self.base_price = base_price

    def get_price(self, demand, peak_threshold):
        if demand > peak_threshold:
            surge = (demand - peak_threshold) * 0.05
            return self.base_price + surge
        return self.base_price