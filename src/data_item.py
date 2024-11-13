# data_item.py
class DataItem:
    def __init__(self, name, unit, value, region, time):
        self.name = name
        self.unit = unit
        self.value = value
        self.region = region
        self.time = time

    def __repr__(self):
        return f"DataItem(name={self.name}, unit={self.unit}, value={self.value}, region={self.region}, time={self.time})"
