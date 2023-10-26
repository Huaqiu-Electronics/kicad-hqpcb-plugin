from dataclasses import dataclass


@dataclass
class PlaceOrderRequest:
    blength: str
    bwidth: str
    type: str = "pcbfile"
