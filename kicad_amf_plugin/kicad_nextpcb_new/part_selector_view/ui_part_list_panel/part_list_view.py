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
            "index", width=60, mode=dv.DATAVIEW_CELL_ACTIVATABLE, align=wx.ALIGN_CENTER
        )
        self.part_list.AppendTextColumn(
            "MPN", width=150, mode=dv.DATAVIEW_CELL_ACTIVATABLE, align=wx.ALIGN_CENTER
        )
        self.part_list.AppendTextColumn(
            "Manufacturer",
            width=250,
            mode=dv.DATAVIEW_CELL_ACTIVATABLE,
            align=wx.ALIGN_CENTER,
        )
        self.part_list.AppendTextColumn(
            "Package/Footprint",
            width=250,
            mode=dv.DATAVIEW_CELL_ACTIVATABLE,
            align=wx.ALIGN_CENTER,
        )
        self.part_list.AppendTextColumn(
            "Category",
            width=150,
            mode=dv.DATAVIEW_CELL_ACTIVATABLE,
            align=wx.ALIGN_CENTER,
        )
        self.part_list.AppendTextColumn(
            "SKU", width=150, mode=dv.DATAVIEW_CELL_ACTIVATABLE, align=wx.ALIGN_CENTER
        )
        self.part_list.AppendTextColumn(
            "Supplier",
            width=150,
            mode=dv.DATAVIEW_CELL_ACTIVATABLE,
            align=wx.ALIGN_CENTER,
        )
        self.part_list.AppendTextColumn(
            "Price(￥)",
            width=150,
            mode=dv.DATAVIEW_CELL_ACTIVATABLE,
            align=wx.ALIGN_CENTER,
        )
        self.part_list.AppendTextColumn(
            "Stock", width=60, mode=dv.DATAVIEW_CELL_ACTIVATABLE, align=wx.ALIGN_CENTER
        )
