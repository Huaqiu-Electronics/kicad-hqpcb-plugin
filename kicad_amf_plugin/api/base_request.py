import dataclasses
import os

@dataclasses.dataclass
class BaseRequest:
    service: str = "pcb"
    region_id: str = "211"  # TODO
    country: str = "211"  # TODO
    express: str = "31"  # TODO


@dataclasses.dataclass
class SmtRequest:
    add_plat_form: str = 5
    patch_file_name: str = ""
    bom_file_name: str = ""
    pcb_file_name: str = ""

    
class SmtFiles:
    patch_file: str = ""
    bom_file: str = ""
    pcb_file: str = ""
