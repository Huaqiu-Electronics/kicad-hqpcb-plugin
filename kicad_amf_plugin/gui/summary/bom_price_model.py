from .price_model_base import PriceModelBase, PriceItem


class BomPriceModel(PriceModelBase):
    bom_price: float = 0

    def data(self, row: int, col: int):
        return 0

    def name(self):
        return _("BOM")

    def sum(self):
        return 0

    def get_items(self) -> "list[PriceItem]":
        return []

    def update(self, data: dict):
        pass
