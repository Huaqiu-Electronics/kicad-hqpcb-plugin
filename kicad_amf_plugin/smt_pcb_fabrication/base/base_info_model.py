from dataclasses import dataclass


@dataclass
class BaseInfoModel:
    # blayer: str  # Layer Count

    # bcount: str  # Qty(single)
    # sidedirection: str  # Decided by the marginMode automatically
    application_sphere: int
    is_pcb_soft_board: str
    single_or_double_technique: str
    number: str
    
    pcb_ban_height: str  # GetPcbLength
    pcb_ban_width: str  # GetPcbWidth
    
    pcb_width: str = ""
    pcb_height: str = ""
    # plate_type: str = "Fr-4"  # Material Type
    # units: str = "2"  # Board Type
    # layoutx: str = None  # X
    # layouty: str = None  # Y
    # sidewidth: str = None  # Break-away Rail

    # testpoint: int = 0  # 测试点数，默认为0
    # board_tg: str = None  # 4层及以上可选TG值，TG130、TG150、TG170
    
    # pbnum: int = None  # 拼版款数，指文件内不同款的板子个数， 不传默认为1


    # edit_size_x
    # edit_size_y


        
