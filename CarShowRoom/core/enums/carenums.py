from .base import BaseEnum


class EngineType(BaseEnum):
    FUEL = 'Fuel'
    DIESEL = 'Diesel'
    HYBRID = 'Hybrid'
    GAS = 'Gas'
    ELECTRICITY = 'Electricity'


class PriceCategory(BaseEnum):
    CHEAP = "Cheap"
    MEDIUM = "Medium"
    LUXURY = "Luxury"
