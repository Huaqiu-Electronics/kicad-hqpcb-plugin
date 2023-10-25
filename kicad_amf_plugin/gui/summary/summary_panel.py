from .ui_summary_panel import UiSummaryPanel
from kicad_amf_plugin.icon import GetImagePath
from kicad_amf_plugin.language.lang_setting_pop_menu import LangSettingPopMenu
import wx
from .order_summary_model import OrderSummary, OrderSummaryModel
from .price_summary_model import PriceSummaryModel

import wx.dataview as dv
from kicad_amf_plugin.settings.setting_manager import SETTING_MANAGER
from kicad_amf_plugin.gui.event.pcb_fabrication_evt_list import (
    UpdatePrice,
    PlaceOrder,
    OrderRegionChanged,
)


class SummaryPanel(UiSummaryPanel):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        self.init_ui()
        self.btn_set_language.Bind(wx.EVT_BUTTON, self.on_set_lang_clicked)
        self.radio_box_order_region.Bind(wx.EVT_RADIOBOX, self.on_region_changed)
        self.btn_update_price.Bind(wx.EVT_BUTTON, self.on_update_price_clicked)
        self.btn_place_order.Bind(wx.EVT_BUTTON, self.on_place_order_clicked)

    def init_ui(self):
        self.list_order_summary.AppendTextColumn(
            _("Build Time"),
            0,
            width=-1,
            mode=dv.DATAVIEW_CELL_ACTIVATABLE,
            align=wx.ALIGN_LEFT,
        )
        self.list_order_summary.AppendTextColumn(
            _("Qty"),
            1,
            width=-1,
            mode=dv.DATAVIEW_CELL_ACTIVATABLE,
            align=wx.ALIGN_CENTER,
        )
        self.list_order_summary.AppendTextColumn(
            _("Price"),
            2,
            width=-1,
            mode=dv.DATAVIEW_CELL_ACTIVATABLE,
            align=wx.ALIGN_LEFT,
        )

        self.list_order_summary.SetMinSize(
            wx.Size(-1, SummaryPanel.GetLineHeight(self) * 3 + 30)
        )
        self.model_order_summary = OrderSummaryModel()
        self.list_order_summary.AssociateModel(self.model_order_summary)

        self.list_price_detail.AppendTextColumn(
            _("Item"),
            0,
            width=120,
            mode=dv.DATAVIEW_CELL_ACTIVATABLE,
            align=wx.ALIGN_LEFT,
        )
        self.list_price_detail.AppendTextColumn(
            _("Price"),
            1,
            width=-1,
            mode=dv.DATAVIEW_CELL_ACTIVATABLE,
            align=wx.ALIGN_RIGHT,
        )

        self.model_price_summary = PriceSummaryModel()
        self.list_price_detail.AssociateModel(self.model_price_summary)
        self.radio_box_order_region.SetSelection(SETTING_MANAGER.order_region)

    def update_price_detail(self, price: "dict"):
        self.model_price_summary.update_price(price)

    def get_total_price(self):
        return self.model_price_summary.get_sum()

    def update_order_summary(self, price_summary: "list"):
        self.model_order_summary.update_order_info(price_summary)

    def on_update_price_clicked(self, ev):
        self.clear_content()
        evt = UpdatePrice(id=-1)
        wx.PostEvent(self.Parent, evt)

    def on_place_order_clicked(self, ev):
        evt = PlaceOrder(id=-1)
        wx.PostEvent(self.Parent, evt)

    def GetImagePath(self, bitmap_path):
        return GetImagePath(bitmap_path)

    @staticmethod
    def GetLineHeight(parent):
        line = wx.TextCtrl(parent)
        _, height = line.GetSize()
        line.Destroy()
        return height

    def on_set_lang_clicked(self, evt):
        menu = LangSettingPopMenu(SETTING_MANAGER.language)
        self.PopupMenu(menu)
        menu.Destroy()

    def clear_content(self):
        for i in self.model_order_summary, self.model_price_summary:
            i.clear_content()

    def on_region_changed(self, evt):
        SETTING_MANAGER.set_order_region(self.radio_box_order_region.GetSelection())
        self.clear_content()
        ev = OrderRegionChanged(-1)
        wx.PostEvent(self.Parent, ev)
