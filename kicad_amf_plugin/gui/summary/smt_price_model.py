from dataclasses import dataclass

from .price_model_base import PriceModelBase, PriceModelCol, PriceItem
from kicad_amf_plugin.utils.number_round import number_round


# TRANSLATED = {
#     0: _("boot_fee"),
#     1: _("project_fee"),
#     2: _("patch_fee"),
#     3: _("space_one_board_fee"),
#     4: _("steel_net_fee"),
#     5: _("plug_fee"),
#     6: _("weld_fee"),
#     7: _("patch_fixture_fee"),
#     8: _("pcb_soft_board_fixture_fee"),
#     9: _("split_board_fixture_fee"),
#     10: _("crimping_fixture_fee"),
#     11: _("fixture_fee"),
#     12: _("fixture_unit_price"),
#     13: _("bom_device_fee"),
#     14: _("confirmal_coating_fee"),
#     15: _("xray_fee"),
#     16: _("ban_split_fee"),
#     17: _("board_clean_fee"),
#     18: _("material_baking_fee"),
#     19: _("increase_tinning_fee"),
#     20: _("check_fee"),
#     21: _("welding_wire_price"),
#     22: _("assembly_weld_fee"),
#     23: _("assemble_price"),
#     24: _("not_assembly_production_fee"),
#     25: _("express_fee"),
#     26: _("packing_fee"),
#     27: _("test_fee"),
#     28: _("program_burning_fee"),
#     29: _("jiaji_price"),
#     30: _("adjust_fee"),
#     31: _("weight"),
#     32: _("total_project_fee"),
#     33: _("total_project_fee_no_tax"),
#     34: _("sum_smt_price"),
#     35: _("sum_spec_price"),
#     36: _("sum_spec_price_no_tax"),
#     37: _("other_price"),
#     38: _("other_price_no_tax"),
#     39: _("smt_price"),
#     40: _("smt_goods_fee"),
#     41: _("smt_goods_fee_no_tax"),
#     42: _("smt_goods_fee_tax"),
#     43: _("smt_order_fee"),
#     44: _("test_return_fee"),
#     45: _("smt_discount_fee"),
#     46: _("single_fee"),
#     47: _("smt_profit"),
#     48: _("total_fee"),
# }

# PROS = {
#     0: "boot_fee",
#     1: "project_fee",
#     2: "patch_fee",
#     3: "space_one_board_fee",
#     4: "steel_net_fee",
#     5: "plug_fee",
#     6: "weld_fee",
#     7: "patch_fixture_fee",
#     8: "pcb_soft_board_fixture_fee",
#     9: "split_board_fixture_fee",
#     10: "crimping_fixture_fee",
#     11: "fixture_fee",
#     12: "fixture_unit_price",
#     13: "bom_device_fee",
#     14: "confirmal_coating_fee",
#     15: "xray_fee",
#     16: "ban_split_fee",
#     17: "board_clean_fee",
#     18: "material_baking_fee",
#     19: "increase_tinning_fee",
#     20: "check_fee",
#     21: "welding_wire_price",
#     22: "assembly_weld_fee",
#     23: "assemble_price",
#     24: "not_assembly_production_fee",
#     25: "express_fee",
#     26: "packing_fee",
#     27: "test_fee",
#     28: "program_burning_fee",
#     29: "jiaji_price",
#     30: "adjust_fee",
#     31: "weight",
#     32: "total_project_fee",
#     33: "total_project_fee_no_tax",
#     34: "sum_smt_price",
#     35: "sum_spec_price",
#     36: "sum_spec_price_no_tax",
#     37: "other_price",
#     38: "other_price_no_tax",
#     39: "smt_price",
#     40: "smt_goods_fee",
#     41: "smt_goods_fee_no_tax",
#     42: "smt_goods_fee_tax",
#     43: "smt_order_fee",
#     44: "test_return_fee",
#     45: "smt_discount_fee",
#     46: "single_fee",
#     47: "smt_profit",
#     48: "total_fee",
# }


# TRANSLATED = {
#     0: _("boot_fee"),
#     1: _("project_fee"),
#     2: _("patch_fee"),
#     3: _("space_one_board_fee"),
#     4: _("steel_net_fee"),
#     5: _("plug_fee"),
#     6: _("weld_fee"),
#     7: _("space_one_board_fee"),
#     8: _("steel_net_fee"),
#     9: _("special_technique_fee"),
#     10: _("confirmal_coating_fee"),
#     11: _("xray_fee"),
#     12: _("ban_split_fee"),
#     13: _("express_fee"),
#     14: _("packing_fee"),
#     15: _("test_fee"),
#     16: _("jiaji_price"),
#     17: _("adjust_fee"),
#     18: _("total_project_fee"),
#     19: _("sum_dip_price"),
#     20: _("sum_pack_exp_price"),
#     21: _("no_plug_discount"),

#     22: _("bom_order_fee"),  
#     23: _("sum_smt_price"),
#     24: _("sum_spec_price"),
#     25: _("other_price"),
#     26: _("test_return_fee"),
#     27: _("smt_order_fee"),
#     28: _("total"),
#     29: _("total_fee"),
# }

# PROS = {
#     0: "boot_fee",
#     1: "project_fee",
#     2: "patch_fee",
#     3: "space_one_board_fee",
#     4: "steel_net_fee",
#     5: "plug_fee",
#     6: "weld_fee",
#     7: "space_one_board_fee",
#     8: "steel_net_fee",
#     9: "special_technique_fee",
#     10: "confirmal_coating_fee",
#     11: "xray_fee",
#     12: "ban_split_fee",
#     13: "express_fee",
#     14: "packing_fee",
#     15: "test_fee",
#     16: "jiaji_price",
#     17: "adjust_fee",
#     18: "total_project_fee",
#     19: "sum_dip_price",
#     20: "sum_pack_exp_price",
#     21: "no_plug_discount",

#     22: "bom_order_fee",
#     23: "sum_smt_price",
#     24: "sum_spec_price",
#     25: "other_price",
#     26: "test_return_fee",
#     27: "smt_order_fee",
#     28: "total",
#     29: "total_fee",
# }




TRANSLATED = {
    # 0: _("plug_fee"),
    # 1: _("total_project_fee"),
    # 2: _("sum_smt_price"),
    # 3: _("sum_spec_price"),
    # 4: _("other_price"),
    # 5: _("smt_price"),
    0: _("total_fee"),
    1: _("total"),
}


PROS = {
    # 0: "plug_fee",
    # 1: "total_project_fee",
    # 2: "sum_smt_price",
    # 3: "sum_spec_price",
    # 4: "other_price",
    # 5: "smt_price",
    0: "total_fee",
    1: "total",
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
        # num = self.prices_item[29].value
        
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

