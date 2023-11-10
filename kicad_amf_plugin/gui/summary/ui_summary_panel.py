# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b3)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.dataview
from kicad_amf_plugin.utils.platebtn import PlateButton, PB_STYLE_GRADIENT
from kicad_amf_plugin.utils.platebtn import (
    PlateButton,
    PB_STYLE_GRADIENT,
    PB_STYLE_SQUARE,
)


###########################################################################
## Class UiSummaryPanel
###########################################################################


class UiSummaryPanel(wx.Panel):
    def __init__(
        self,
        parent,
        id=wx.ID_ANY,
        pos=wx.DefaultPosition,
        size=wx.Size(-1, -1),
        style=wx.TAB_TRAVERSAL,
        name=wx.EmptyString,
    ):
        wx.Panel.__init__(
            self, parent, id=id, pos=pos, size=size, style=style, name=name
        )

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        bSizer3 = wx.BoxSizer(wx.HORIZONTAL)

        sbSizer4 = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("Preference")), wx.HORIZONTAL
        )

        self.m_staticText1 = wx.StaticText(
            sbSizer4.GetStaticBox(),
            wx.ID_ANY,
            _("Website"),
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_staticText1.Wrap(-1)

        sbSizer4.Add(self.m_staticText1, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        choice_order_regionChoices = []
        self.choice_order_region = wx.Choice(
            sbSizer4.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            choice_order_regionChoices,
            0,
        )
        self.choice_order_region.SetSelection(0)
        sbSizer4.Add(self.choice_order_region, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        sbSizer4.Add((0, 0), 1, wx.EXPAND, 5)

        bSizer3.Add(sbSizer4, 1, wx.EXPAND, 5)

        bSizer1.Add(bSizer3, 0, wx.EXPAND, 5)

        self.splitter_detail_summary = wx.SplitterWindow(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_LIVE_UPDATE
        )
        self.splitter_detail_summary.Bind(
            wx.EVT_IDLE, self.splitter_detail_summaryOnIdle
        )

        self.m_panel1 = wx.Panel(
            self.splitter_detail_summary,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TAB_TRAVERSAL,
        )
        sbSizer1 = wx.StaticBoxSizer(
            wx.StaticBox(self.m_panel1, wx.ID_ANY, _("Cost detail")), wx.VERTICAL
        )

        self.list_price_detail = wx.dataview.DataViewCtrl(
            sbSizer1.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.dataview.DV_ROW_LINES | wx.dataview.DV_VERT_RULES,
        )
        sbSizer1.Add(self.list_price_detail, 1, wx.ALL | wx.EXPAND, 5)

        self.m_panel1.SetSizer(sbSizer1)
        self.m_panel1.Layout()
        sbSizer1.Fit(self.m_panel1)
        self.m_panel2 = wx.Panel(
            self.splitter_detail_summary,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TAB_TRAVERSAL,
        )
        sbSizer41 = wx.StaticBoxSizer(
            wx.StaticBox(self.m_panel2, wx.ID_ANY, _("Order Summary")), wx.VERTICAL
        )

        self.list_order_summary = wx.dataview.DataViewCtrl(
            sbSizer41.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.dataview.DV_ROW_LINES | wx.dataview.DV_VERT_RULES,
        )
        sbSizer41.Add(self.list_order_summary, 1, wx.ALL | wx.EXPAND, 5)

        self.m_panel2.SetSizer(sbSizer41)
        self.m_panel2.Layout()
        sbSizer41.Fit(self.m_panel2)
        self.splitter_detail_summary.SplitHorizontally(self.m_panel1, self.m_panel2, 0)
        bSizer1.Add(self.splitter_detail_summary, 1, wx.EXPAND, 5)

        bSizer31 = wx.BoxSizer(wx.VERTICAL)

        self.btn_update_price = PlateButton(
            self,
            bmp=wx.Bitmap(self.GetImagePath("query.png"), wx.BITMAP_TYPE_ANY),
            style=PB_STYLE_GRADIENT,
            label=_("Update Price"),
        )
        bSizer31.Add(self.btn_update_price, 1, wx.ALL | wx.EXPAND, 5)

        self.btn_place_order = PlateButton(
            self,
            bmp=wx.Bitmap(self.GetImagePath("cart.png"), wx.BITMAP_TYPE_ANY),
            style=PB_STYLE_GRADIENT,
            label=_("Add to Cart"),
        )
        bSizer31.Add(self.btn_place_order, 1, wx.ALL | wx.EXPAND, 5)

        bSizer1.Add(bSizer31, 0, wx.EXPAND, 5)

        self.SetSizer(bSizer1)
        self.Layout()
        bSizer1.Fit(self)

    def __del__(self):
        pass

    def splitter_detail_summaryOnIdle(self, event):
        self.splitter_detail_summary.SetSashPosition(0)
        self.splitter_detail_summary.Unbind(wx.EVT_IDLE)

    # Virtual image path resolution method. Override this in your derived class.
    def GetImagePath(self, bitmap_path):
        return bitmap_path
