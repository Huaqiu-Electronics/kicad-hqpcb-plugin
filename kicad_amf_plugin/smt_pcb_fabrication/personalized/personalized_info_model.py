from dataclasses import dataclass


@dataclass
class PersonalizedInfoModel:

    solder_paste_type: str
    is_assembly_weld: str
    is_layout_cleaning: str
    is_material_baking: str
    is_welding_wire: str
    is_test: str
    is_assemble: str
    is_program_burning: str
    need_split: str       # 拆板出货
    is_increase_tinning: str
    need_conformal_coating: str   # 刷三防漆
    is_first_confirm: str
    packing_type: str
    
    pcb_width: str = ""   # pcb单片宽
    pcb_height: str = ""   # pcb单片长
    
    postscript: str = ""
    test_duration: str =""
    x_ray_unit_number: str = 1
    x_ray_number: str = 1
        




