import wx
import wx.dataview

from kicad_amf_plugin.kicad_nextpcb_new.helpers import (
    PLUGIN_PATH,
    HighResWxSize,
)


class FootPrintList(wx.dataview.DataViewListCtrl):
    def __init__(
        self,
        parent,
        mainwindows,
        id=wx.ID_ANY,
        pos=wx.DefaultPosition,
        size=wx.DefaultSize,
        style=wx.dataview.DV_MULTIPLE,
    ):
        wx.dataview.DataViewListCtrl.__init__(self, parent, id, pos, size, style)

        self.SetMinSize(HighResWxSize(mainwindows.window, wx.Size(900, 400)))
        self.idx = self.AppendTextColumn(
            "index",
            mode=wx.dataview.DATAVIEW_CELL_INERT,
            width=int(mainwindows.scale_factor * 50),
            align=wx.ALIGN_CENTER,
            flags=wx.dataview.DATAVIEW_COL_RESIZABLE,
        )
        self.reference = self.AppendTextColumn(
            "Reference",
            mode=wx.dataview.DATAVIEW_CELL_INERT,
            width=int(mainwindows.scale_factor * 80),
            align=wx.ALIGN_CENTER,
            flags=wx.dataview.DATAVIEW_COL_RESIZABLE,
        )
        self.value = self.AppendTextColumn(
            "Value",
            mode=wx.dataview.DATAVIEW_CELL_INERT,
            width=int(mainwindows.scale_factor * 100),
            align=wx.ALIGN_CENTER,
            flags=wx.dataview.DATAVIEW_COL_RESIZABLE,
        )
        self.footprint = self.AppendTextColumn(
            "Footprint",
            mode=wx.dataview.DATAVIEW_CELL_INERT,
            width=int(mainwindows.scale_factor * 300),
            align=wx.ALIGN_CENTER,
            flags=wx.dataview.DATAVIEW_COL_RESIZABLE,
        )
        self.lcsc = self.AppendTextColumn(
            "MPN",
            mode=wx.dataview.DATAVIEW_CELL_INERT,
            width=int(mainwindows.scale_factor * 200),
            align=wx.ALIGN_CENTER,
            flags=wx.dataview.DATAVIEW_COL_RESIZABLE,
        )
        self.type_column = self.AppendTextColumn(
            "Manufacturer",
            mode=wx.dataview.DATAVIEW_CELL_INERT,
            width=int(mainwindows.scale_factor * 200),
            align=wx.ALIGN_CENTER,
            flags=wx.dataview.DATAVIEW_COL_RESIZABLE,
        )
        self.stock = self.AppendTextColumn(
            "Category",
            mode=wx.dataview.DATAVIEW_CELL_INERT,
            width=int(mainwindows.scale_factor * 200),
            align=wx.ALIGN_CENTER,
            flags=wx.dataview.DATAVIEW_COL_RESIZABLE,
        )
        self.stock = self.AppendTextColumn(
            "SKU",
            mode=wx.dataview.DATAVIEW_CELL_INERT,
            width=int(mainwindows.scale_factor * 150),
            align=wx.ALIGN_CENTER,
            flags=wx.dataview.DATAVIEW_COL_RESIZABLE,
        )
        self.stock = self.AppendTextColumn(
            "Supplier",
            mode=wx.dataview.DATAVIEW_CELL_INERT,
            width=int(mainwindows.scale_factor * 150),
            align=wx.ALIGN_CENTER,
            flags=wx.dataview.DATAVIEW_COL_RESIZABLE,
        )
        self.stock = self.AppendTextColumn(
            "Quantity",
            mode=wx.dataview.DATAVIEW_CELL_INERT,
            width=int(mainwindows.scale_factor * 80),
            align=wx.ALIGN_CENTER,
            flags=wx.dataview.DATAVIEW_COL_RESIZABLE,
        )
        self.bom = self.AppendToggleColumn(
            "BOM",
            mode=wx.dataview.DATAVIEW_CELL_ACTIVATABLE,
            width=int(mainwindows.scale_factor * 60),
            align=wx.ALIGN_CENTER,
            flags=wx.dataview.DATAVIEW_COL_RESIZABLE,
        )
        self.pos = self.AppendToggleColumn(
            "POS",
            mode=wx.dataview.DATAVIEW_CELL_ACTIVATABLE,
            width=int(mainwindows.scale_factor * 60),
            align=wx.ALIGN_CENTER,
            flags=wx.dataview.DATAVIEW_COL_RESIZABLE,
        )
        self.rot = self.AppendTextColumn(
            "Rotation",
            mode=wx.dataview.DATAVIEW_CELL_INERT,
            width=int(mainwindows.scale_factor * 80),
            align=wx.ALIGN_CENTER,
            flags=wx.dataview.DATAVIEW_COL_RESIZABLE,
        )
        self.side = self.AppendTextColumn(
            "Side",
            mode=wx.dataview.DATAVIEW_CELL_INERT,
            width=int(mainwindows.scale_factor * 50),
            align=wx.ALIGN_CENTER,
            flags=wx.dataview.DATAVIEW_COL_RESIZABLE,
        )

        self.AppendTextColumn(
            "",
            mode=wx.dataview.DATAVIEW_CELL_INERT,
            width=1,
            align=wx.ALIGN_CENTER,
            flags=wx.dataview.DATAVIEW_COL_RESIZABLE,
        )
