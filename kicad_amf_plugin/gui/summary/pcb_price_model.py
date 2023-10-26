from dataclasses import dataclass

from .price_model_base import PriceModelBase, PriceModelCol, PriceItem
from kicad_amf_plugin.utils.number_round import number_round

TRANSLATED = {
    0: _("testfee"),
    1: _("plate"),
    2: _("clc"),
    3: _("gch"),
    4: _("bgafee"),
    5: _("impendancefee"),
    6: _("pin"),
    7: _("copperfee"),
    8: _("colorfee"),
    9: _("sprayfee"),
    10: _("extraurgentfee"),
    11: _("viasfee"),
    12: _("bankongfee"),
    13: _("utilizationfee"),
    14: _("discountfee"),
    15: _("boardfee"),
    16: _("difficultyfee"),
    17: _("coverfee"),
    18: _("blindfee"),
    19: _("pressingfee"),
    20: _("cjfee"),
    21: _("pthfee"),
    22: _("viainpadfee"),
    23: _("reportfee"),
    24: _("populerfee"),
    25: _("paperfee"),
    26: _("userstampfee"),
    27: _("acceptancefee"),
    28: _("crossfee"),
    29: _("invoicefee"),
    30: _("insurancefee"),
    31: _("zkfee"),
    32: _("cutfee"),
    33: _("luocao"),
    34: _("luocheng"),
}


PROS = {
    0: "testfee",
    1: "plate",
    2: "clc",
    3: "gch",
    4: "bgafee",
    5: "impendancefee",
    6: "pin",
    7: "copperfee",
    8: "colorfee",
    9: "sprayfee",
    10: "extraurgentfee",
    11: "viasfee",
    12: "bankongfee",
    13: "utilizationfee",
    14: "discountfee",
    15: "boardfee",
    16: "difficultyfee",
    17: "coverfee",
    18: "blindfee",
    19: "pressingfee",
    20: "cjfee",
    21: "pthfee",
    22: "viainpadfee",
    23: "reportfee",
    24: "populerfee",
    25: "paperfee",
    26: "userstampfee",
    27: "acceptancefee",
    28: "crossfee",
    29: "invoicefee",
    30: "insurancefee",
    31: "zkfee",
    32: "cutfee",
    33: "luocao",
    34: "luocheng",
}


class PCBPriceModel(PriceModelBase):
    def __init__(self) -> None:
        super().__init__()
        self.prices_item: "list[PriceItem]" = []
        for i in TRANSLATED:
            self.prices_item.append(PriceItem(PROS[i], TRANSLATED[i], 0, self))

    def data(self, row: int, col: int):
        if col == PriceModelCol.VALUE:
            return self.prices_item[row]
        elif col == PriceModelCol.DESC:
            return TRANSLATED[row]

    def name(self):
        return "PCB"

    @number_round()
    def sum(self):
        num = 0
        for i in self.prices_item:
            num = num + i.value
        return num

    def get_items(self) -> "list[PriceItem]":
        return [i for i in self.prices_item if i.value]

    def update(self, data: dict):
        for i in PROS:
            if PROS[i] in data:
                self.prices_item[i].value = data[PROS[i]]

    def item_names(self):
        return PROS

    def clear(self):
        for i in self.prices_item:
            i.value = 0
