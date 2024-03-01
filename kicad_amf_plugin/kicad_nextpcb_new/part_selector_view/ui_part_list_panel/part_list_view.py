import wx
import wx.xrc
import wx.dataview
from .ui_part_list_panel import UiPartListPanel
import wx.dataview as dv


class PartListView(UiPartListPanel):
    def __init__(
        self,
        parent,
        id=wx.ID_ANY,
        pos=wx.DefaultPosition,
        size=wx.DefaultSize,
        style=wx.TAB_TRAVERSAL,
        name=wx.EmptyString,
    ):
        super().__init__(parent, id=id, pos=pos, size=size, style=style, name=name)

        self.part_list.AppendTextColumn(
            _("index"), width=60, mode=dv.DATAVIEW_CELL_ACTIVATABLE, align=wx.ALIGN_CENTER
        )
        self.part_list.AppendTextColumn(
            _("MPN"), width=150, mode=dv.DATAVIEW_CELL_ACTIVATABLE, align=wx.ALIGN_CENTER
        )
        self.part_list.AppendTextColumn(
            _("Manufacturer"),
            width=250,
            mode=dv.DATAVIEW_CELL_ACTIVATABLE,
            align=wx.ALIGN_CENTER,
        )
        self.part_list.AppendTextColumn(
            _("Package/Footprint"),
            width=250,
            mode=dv.DATAVIEW_CELL_ACTIVATABLE,
            align=wx.ALIGN_CENTER,
        )
        self.part_list.AppendTextColumn(
            _("Category"),
            width=150,
            mode=dv.DATAVIEW_CELL_ACTIVATABLE,
            align=wx.ALIGN_CENTER,
        )
        self.part_list.AppendTextColumn(
            _("SKU"), width=150, mode=dv.DATAVIEW_CELL_ACTIVATABLE, align=wx.ALIGN_CENTER
        )
        self.part_list.AppendTextColumn(
            _("Supplier"),
            width=150,
            mode=dv.DATAVIEW_CELL_ACTIVATABLE,
            align=wx.ALIGN_CENTER,
        )
        self.part_list.AppendTextColumn(
            _("Price")+ "(￥)",
            width=150,
            mode=dv.DATAVIEW_CELL_ACTIVATABLE,
            align=wx.ALIGN_CENTER,
        )
        self.part_list.AppendTextColumn(
            _("Stock"), width=60, mode=dv.DATAVIEW_CELL_ACTIVATABLE, align=wx.ALIGN_CENTER
        )
