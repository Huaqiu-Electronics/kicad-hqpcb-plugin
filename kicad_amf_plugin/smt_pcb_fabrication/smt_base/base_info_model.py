from dataclasses import dataclass


@dataclass
class BaseInfoModel:
    
    application_sphere: int
    is_pcb_soft_board: str
    single_or_double_technique: str
    custom_pcb_ban: str 
    bom_purchase: str 
    number: str
    
    pcb_ban_height: str  # GetPcbLength
    pcb_ban_width: str  # GetPcbWidth
     
    pcb_width: str = ""   # pcb单片宽
    pcb_height: str = ""   # pcb单片长
    


        
