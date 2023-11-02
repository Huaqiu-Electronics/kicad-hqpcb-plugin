# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b3)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
from kicad_amf_plugin.utils.platebtn import PlateButton, PB_STYLE_GRADIENT
import wx.dataview
from kicad_amf_plugin.utils.platebtn import (
    PlateButton,
    PB_STYLE_GRADIENT,
    PB_STYLE_SQUARE,
)

import gettext

_ = gettext.gettext

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

        radio_box_order_regionChoices = [_("CN"), _("JP"), _("EU/USA")]
        self.radio_box_order_region = wx.RadioBox(
            sbSizer4.GetStaticBox(),
            wx.ID_ANY,
            _("Order Region"),
            wx.DefaultPosition,
            wx.DefaultSize,
            radio_box_order_regionChoices,
            1,
            wx.RA_SPECIFY_ROWS,
        )
        self.radio_box_order_region.SetSelection(0)
        sbSizer4.Add(self.radio_box_order_region, 0, 0, 5)

        sbSizer4.Add((0, 0), 1, wx.EXPAND, 5)

        self.btn_set_language = PlateButton(
            self,
            bmp=wx.Bitmap(self.GetImagePath("language.png"), wx.BITMAP_TYPE_ANY),
            style=PB_STYLE_GRADIENT,
        )
        sbSizer4.Add(self.btn_set_language, 0, wx.ALL, 5)

        bSizer3.Add(sbSizer4, 1, wx.EXPAND, 5)

        bSizer1.Add(bSizer3, 0, wx.EXPAND, 5)

        sbSizer1 = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("Cost detail")), wx.VERTICAL
        )

        self.list_price_detail = wx.dataview.DataViewCtrl(
            sbSizer1.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.dataview.DV_ROW_LINES | wx.dataview.DV_VERT_RULES,
        )
        sbSizer1.Add(self.list_price_detail, 1, wx.ALL | wx.EXPAND, 5)

        bSizer1.Add(sbSizer1, 1, wx.EXPAND, 5)

        sbSizer41 = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("Order Summary")), wx.VERTICAL
        )

        self.list_order_summary = wx.dataview.DataViewCtrl(
            sbSizer41.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.dataview.DV_ROW_LINES | wx.dataview.DV_VERT_RULES,
        )
        sbSizer41.Add(self.list_order_summary, 1, wx.ALL | wx.EXPAND, 5)

        bSizer1.Add(sbSizer41, 0, wx.EXPAND | wx.FIXED_MINSIZE, 5)

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

    # Virtual image path resolution method. Override this in your derived class.
    def GetImagePath(self, bitmap_path):
        return bitmap_path
