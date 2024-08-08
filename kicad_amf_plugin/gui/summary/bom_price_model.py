from .price_model_base import PriceModelBase, PriceItem

TRANSLATED = {
    0: _("total"),
}


PROS = {
    0: "total",
}
class BomPriceModel(PriceModelBase):
    def __init__(self) -> None:
        super().__init__()
        self.bom_price : float = 0


    def data(self, row: int, col: int):
        return 0

    def name(self):
        return _("BOM")
    

    def sum(self):
        num = 0
        # for i in self.prices_item:
        #     num = num + i.value
        # num = round(num, 2)
        num = round(self.bom_price, 2)
        return num

    def get_items(self) -> "list[PriceItem]":
        return []

    def update(self, data: dict):
        pass

    def set_visibility(self, visibility):
        pass

    def update_with_total_prices(self, total_prices):
        print("Total prices received:", total_prices)
        self.bom_price = total_prices
 