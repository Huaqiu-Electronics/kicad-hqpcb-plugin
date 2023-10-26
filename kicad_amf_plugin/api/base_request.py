import dataclasses


@dataclasses.dataclass
class BaseRequest:
    service: str = "pcb"
    region_id: str = "211"  # TODO
    country: str = "211"  # TODO
    express: str = "31"  # TODO
