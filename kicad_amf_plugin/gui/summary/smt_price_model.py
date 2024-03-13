from dataclasses import dataclass

from .price_model_base import PriceModelBase, PriceModelCol, PriceItem
from kicad_amf_plugin.utils.number_round import number_round


TRANSLATED = {
    # 0: _("total_fee"),
    0: _("smt_goods_fee_no_tax"),
    1: _("total"),
    2: _("smt_goods_fee_tax"),
}


PROS = {
    # 0: "total_fee",
    0: "smt_goods_fee_no_tax",
    1: "total",
    2: "smt_goods_fee_tax",
}


class SmtPriceModel(PriceModelBase):
    def __init__(self) -> None:
        super().__init__()
        self.prices_item: "list[PriceItem]" = []
        for i in TRANSLATED:
            self.prices_item.append(PriceItem(PROS[i], TRANSLATED[i], 0, self))

    smt_price: float = 0

    def data(self, row: int, col: int):
        if col == PriceModelCol.VALUE:
            return self.prices_item[row]
        elif col == PriceModelCol.DESC:
            return TRANSLATED[row]


    def name(self):
        return _("SMT")

    def sum(self):
        num = 0
        for i in self.prices_item:
            num = num + i.value
        num = round(num, 2)
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

