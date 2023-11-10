from kicad_amf_plugin.order.supported_region import SupportedRegion
from kicad_amf_plugin.utils.roles import EditDisplayRole
from .ui_summary_panel import UiSummaryPanel
from kicad_amf_plugin.icon import GetImagePath
import wx
from .order_summary_model import OrderSummaryModel
from .price_summary_model import PriceSummaryModel


import wx.dataview as dv
from kicad_amf_plugin.settings.setting_manager import SETTING_MANAGER
from kicad_amf_plugin.gui.event.pcb_fabrication_evt_list import (
    UpdatePrice,
    PlaceOrder,
    OrderRegionChanged,
)


OrderRegionSettings = (
    EditDisplayRole(SupportedRegion.CHINA_MAINLAND, _("Mainland China")),
    EditDisplayRole(SupportedRegion.EUROPE_USA, _("Worldwide (English)")),
    EditDisplayRole(SupportedRegion.JAPAN, _("Worldwide (Japanese)")),
)


class SummaryPanel(UiSummaryPanel):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        self.init_ui()
        self.btn_update_price.Bind(wx.EVT_BUTTON, self.on_update_price_clicked)
        self.btn_place_order.Bind(wx.EVT_BUTTON, self.on_place_order_clicked)
        self.choice_order_region.Bind(wx.EVT_CHOICE, self.on_region_changed)
        self.Bind(
            wx.EVT_SPLITTER_SASH_POS_CHANGED,
            self.on_sash_changed,
            self.splitter_detail_summary,
        )

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
        self.choice_order_region.AppendItems(
            [i.DisplayRole for i in OrderRegionSettings]
        )
        self.choice_order_region.SetSelection(SETTING_MANAGER.order_region)

        max_width = 300
        for view in self.list_order_summary, self.list_price_detail:
            sum = 0
            for i in range(0, view.GetColumnCount()):
                sum = sum + view.GetColumn(i).GetWidth()
            max_width = max(max_width, sum)
            sum = 0

        self.SetMinSize(wx.Size(max_width + 30, -1))

    def splitter_detail_summaryOnIdle(self, event):
        self.splitter_detail_summary.SetSashPosition(
            SETTING_MANAGER.get_summary_detail_sash_pos()
        )
        self.splitter_detail_summary.Unbind(wx.EVT_IDLE)

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

    def on_sash_changed(self, evt):
        sash_pos = evt.GetSashPosition()
        SETTING_MANAGER.set_summary_detail_sash_pos(sash_pos)

    def GetImagePath(self, bitmap_path):
        return GetImagePath(bitmap_path)

    @staticmethod
    def GetLineHeight(parent):
        line = wx.TextCtrl(parent)
        _, height = line.GetSize()
        line.Destroy()
        return height

    def clear_content(self):
        for i in self.model_order_summary, self.model_price_summary:
            i.clear_content()

    def on_region_changed(self, evt):
        SETTING_MANAGER.set_order_region(self.choice_order_region.GetCurrentSelection())
        self.clear_content()
        ev = OrderRegionChanged(-1)
        wx.PostEvent(self.Parent, ev)
