from dataclasses import dataclass


@dataclass
class SpecialProcessModel:
    impendance: str  # Impendance
    bankong: str  # Plated Half Holes:
    blind: str  # HDI(Buried/blind vias):
    via_in_pad: str  # Pad Hole:
    beveledge: str  # Beveling of G/F:
    pressing: str = ""  # Stack up

    baobian: str = None  # 包边，默认 0 无 1-4 边
    bga: str = None  # BGA，默认0 无，可选值 0.35 – 0.35及以上 0.25  #CN only
    zknum: str = None  # 钻孔密度
