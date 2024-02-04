from dataclasses import dataclass


@dataclass
class PersonalizedInfoModel:
    # test: str  # Electrical Test
    # shipment_report: str  # Delivery Report
    # slice_report: str  # Microsection Analysis Report
    # report_type: str  # Report Format
    # review_file: str  # Approve Working Gerber:  确认生产稿 0无需 1需要-自动确认 2需要-非自动确认
    # has_period: str  # Decided by period_format
    # period_format: str or None  # UL Mark
    # film_report: str  # Film
    # pcb_note: str  # Special Requests # Non-CN

    # cross_board: int  # 打叉板 1接受 2不接受
    # paper: int  # 隔白纸 1无需 2需要
    # user_stamp: int  # 不加客编 1无要求 2指定位置加客编 3不加客编
    # hq_pack: int = None  # 包装要求，默认 1华秋包装，0中性包装  #CN only


    solder_paste_type: str
    is_assembly_weld: str
    is_layout_cleaning: str
    is_material_baking: str
    is_welding_wire: str
    is_test: str
    is_assemble: str
    is_program_burning: str
    need_split: str
    is_increase_tinning: str
    need_conformal_coating: str
    is_first_confirm: str
    packing_type: str
    
    postscript: str = ""
    test_duration: str =""
    x_ray_unit_number: str = 1
    x_ray_number: str = 1
        




