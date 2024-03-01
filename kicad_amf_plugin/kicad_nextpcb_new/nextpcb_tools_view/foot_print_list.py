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
            _("index"),
            mode=wx.dataview.DATAVIEW_CELL_INERT,
            width=int(mainwindows.scale_factor * 50),
            align=wx.ALIGN_CENTER,
            flags=wx.dataview.DATAVIEW_COL_RESIZABLE,
        )
        self.reference = self.AppendTextColumn(
            _("Reference"),
            mode=wx.dataview.DATAVIEW_CELL_INERT,
            width=int(mainwindows.scale_factor * 80),
            align=wx.ALIGN_CENTER,
            flags=wx.dataview.DATAVIEW_COL_RESIZABLE,
        )
        self.value = self.AppendTextColumn(
            _("Value"),
            mode=wx.dataview.DATAVIEW_CELL_INERT,
            width=int(mainwindows.scale_factor * 100),
            align=wx.ALIGN_CENTER,
            flags=wx.dataview.DATAVIEW_COL_RESIZABLE,
        )
        self.footprint = self.AppendTextColumn(
            _("Footprint"),
            mode=wx.dataview.DATAVIEW_CELL_INERT,
            width=int(mainwindows.scale_factor * 300),
            align=wx.ALIGN_CENTER,
            flags=wx.dataview.DATAVIEW_COL_RESIZABLE,
        )
        self.colu_mpn = self.AppendTextColumn(
            _("MPN"),
            mode=wx.dataview.DATAVIEW_CELL_INERT,
            width=int(mainwindows.scale_factor * 200),
            align=wx.ALIGN_CENTER,
            flags=wx.dataview.DATAVIEW_COL_RESIZABLE,
        )
        self.colu_manufact = self.AppendTextColumn(
            _("Manufacturer"),
            mode=wx.dataview.DATAVIEW_CELL_INERT,
            width=int(mainwindows.scale_factor * 200),
            align=wx.ALIGN_CENTER,
            flags=wx.dataview.DATAVIEW_COL_RESIZABLE,
        )
        self.colu_category = self.AppendTextColumn(
            _("Category"),
            mode=wx.dataview.DATAVIEW_CELL_INERT,
            width=int(mainwindows.scale_factor * 200),
            align=wx.ALIGN_CENTER,
            flags=wx.dataview.DATAVIEW_COL_RESIZABLE,
        )
        self.colu_sku = self.AppendTextColumn(
            _("SKU"),
            mode=wx.dataview.DATAVIEW_CELL_INERT,
            width=int(mainwindows.scale_factor * 150),
            align=wx.ALIGN_CENTER,
            flags=wx.dataview.DATAVIEW_COL_RESIZABLE,
        )
        self.colu_supplier = self.AppendTextColumn(
            _("Supplier"),
            mode=wx.dataview.DATAVIEW_CELL_INERT,
            width=int(mainwindows.scale_factor * 150),
            align=wx.ALIGN_CENTER,
            flags=wx.dataview.DATAVIEW_COL_RESIZABLE,
        )
        self.colu_quantity = self.AppendTextColumn(
            _("Quantity"),
            mode=wx.dataview.DATAVIEW_CELL_INERT,
            width=int(mainwindows.scale_factor * 80),
            align=wx.ALIGN_CENTER,
            flags=wx.dataview.DATAVIEW_COL_RESIZABLE,
        )
        self.bom = self.AppendToggleColumn(
            _("BOM"),
            mode=wx.dataview.DATAVIEW_CELL_ACTIVATABLE,
            width=int(mainwindows.scale_factor * 60),
            align=wx.ALIGN_CENTER,
            flags=wx.dataview.DATAVIEW_COL_RESIZABLE,
        )
        self.pos = self.AppendToggleColumn(
            _("POS"),
            mode=wx.dataview.DATAVIEW_CELL_ACTIVATABLE,
            width=int(mainwindows.scale_factor * 60),
            align=wx.ALIGN_CENTER,
            flags=wx.dataview.DATAVIEW_COL_RESIZABLE,
        )
        self.rot = self.AppendTextColumn(
            _("Rotation"),
            mode=wx.dataview.DATAVIEW_CELL_INERT,
            width=int(mainwindows.scale_factor * 80),
            align=wx.ALIGN_CENTER,
            flags=wx.dataview.DATAVIEW_COL_RESIZABLE,
        )
        self.side = self.AppendTextColumn(
            _("Side"),
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
