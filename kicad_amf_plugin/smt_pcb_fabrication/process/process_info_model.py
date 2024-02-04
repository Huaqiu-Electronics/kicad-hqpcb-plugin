from dataclasses import dataclass


@dataclass
class ProcessInfoModel:
    # bheight: str  # PCB Thickness
    # copper: str  # Finished Copper Weight
    # lineweight: str  # Min Trace/Space Outer
    # vias: str  # Min Drilled Hole
    # color: str  # Solder Mask Color
    # charcolor: str  # Silkscreen
    # cover: str  # Via Process
    # spray: str  # Surface Finish
    # insidecopper: str = "0"  # Inner Copper Weight
    # cjh: str = None  # SurfaceProcessCtrl
    is_plug: str 
    steel_type: str 
    is_steel_follow_delivery: str

    bom_material_type_number: str = 1
    patch_pad_number : str  = 1
    plug_number: str  = 1
