# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b3)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc


###########################################################################
## Class UiProcessInfo
###########################################################################


class UiProcessInfo(wx.Panel):
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

        labelProcessInfo = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("Process info")), wx.VERTICAL
        )

        fgSizer25 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer25.AddGrowableCol(1)
        fgSizer25.SetFlexibleDirection(wx.BOTH)
        fgSizer25.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.label_pcb_thick = wx.StaticText(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            _("PCB Thickness"),
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.label_pcb_thick.Wrap(-1)

        fgSizer25.Add(self.label_pcb_thick, 0, wx.ALL, 5)

        fgSizer26 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer26.AddGrowableCol(0)
        fgSizer26.SetFlexibleDirection(wx.BOTH)
        fgSizer26.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        combo_board_thicknessChoices = []
        self.combo_board_thickness = wx.Choice(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            combo_board_thicknessChoices,
            0,
        )
        self.combo_board_thickness.SetSelection(0)
        fgSizer26.Add(self.combo_board_thickness, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText41 = wx.StaticText(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            _("mm"),
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_staticText41.Wrap(-1)

        fgSizer26.Add(self.m_staticText41, 0, wx.ALL, 5)

        fgSizer25.Add(fgSizer26, 1, wx.EXPAND, 5)

        self.m_staticText401 = wx.StaticText(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            _("FInsihed Copper weight"),
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_staticText401.Wrap(-1)

        fgSizer25.Add(self.m_staticText401, 0, wx.ALL, 5)

        combo_outer_copper_thicknessChoices = []
        self.combo_outer_copper_thickness = wx.Choice(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            combo_outer_copper_thicknessChoices,
            0,
        )
        self.combo_outer_copper_thickness.SetSelection(0)
        fgSizer25.Add(self.combo_outer_copper_thickness, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText4011 = wx.StaticText(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            _("Inner Copper Weight"),
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_staticText4011.Wrap(-1)

        fgSizer25.Add(self.m_staticText4011, 0, wx.ALL, 5)

        combo_inner_copper_thicknessChoices = []
        self.combo_inner_copper_thickness = wx.Choice(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            combo_inner_copper_thicknessChoices,
            0,
        )
        self.combo_inner_copper_thickness.SetSelection(0)
        fgSizer25.Add(self.combo_inner_copper_thickness, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText40111 = wx.StaticText(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            _("Min Trace/Space Outer"),
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_staticText40111.Wrap(-1)

        fgSizer25.Add(self.m_staticText40111, 0, wx.ALL, 5)

        combo_min_trace_width_clearanceChoices = []
        self.combo_min_trace_width_clearance = wx.Choice(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            combo_min_trace_width_clearanceChoices,
            0,
        )
        self.combo_min_trace_width_clearance.SetSelection(0)
        fgSizer25.Add(self.combo_min_trace_width_clearance, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText401111 = wx.StaticText(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            _("Min Drilled Hole"),
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_staticText401111.Wrap(-1)

        fgSizer25.Add(self.m_staticText401111, 0, wx.ALL, 5)

        combo_min_hole_sizeChoices = []
        self.combo_min_hole_size = wx.Choice(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            combo_min_hole_sizeChoices,
            0,
        )
        self.combo_min_hole_size.SetSelection(0)
        fgSizer25.Add(self.combo_min_hole_size, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText4011111 = wx.StaticText(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            _("Solder Mask Color"),
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_staticText4011111.Wrap(-1)

        fgSizer25.Add(self.m_staticText4011111, 0, wx.ALL, 5)

        combo_solder_colorChoices = []
        self.combo_solder_color = wx.Choice(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            combo_solder_colorChoices,
            0,
        )
        self.combo_solder_color.SetSelection(0)
        fgSizer25.Add(self.combo_solder_color, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText40111111 = wx.StaticText(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            _("Silkscreen"),
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_staticText40111111.Wrap(-1)

        fgSizer25.Add(self.m_staticText40111111, 0, wx.ALL, 5)

        combo_silk_screen_colorChoices = []
        self.combo_silk_screen_color = wx.Choice(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            combo_silk_screen_colorChoices,
            0,
        )
        self.combo_silk_screen_color.SetSelection(0)
        fgSizer25.Add(self.combo_silk_screen_color, 0, wx.ALL | wx.EXPAND, 5)

        self.label_stackup = wx.StaticText(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            _("Via Process"),
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.label_stackup.Wrap(-1)

        fgSizer25.Add(self.label_stackup, 0, wx.ALL, 5)

        combo_solder_coverChoices = []
        self.combo_solder_cover = wx.Choice(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            combo_solder_coverChoices,
            0,
        )
        self.combo_solder_cover.SetSelection(0)
        fgSizer25.Add(self.combo_solder_cover, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText4011111111 = wx.StaticText(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            _("Surface Finish"),
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_staticText4011111111.Wrap(-1)

        fgSizer25.Add(self.m_staticText4011111111, 0, wx.ALL, 5)

        combo_surface_processChoices = []
        self.combo_surface_process = wx.Choice(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            combo_surface_processChoices,
            0,
        )
        self.combo_surface_process.SetSelection(0)
        fgSizer25.Add(self.combo_surface_process, 0, wx.ALL | wx.EXPAND, 5)

        self.label_immersion_gold = wx.StaticText(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            _("Immersion Gold Thickness"),
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.label_immersion_gold.Wrap(-1)

        fgSizer25.Add(self.label_immersion_gold, 0, wx.ALL, 5)

        combo_gold_thicknessChoices = []
        self.combo_gold_thickness = wx.Choice(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            combo_gold_thicknessChoices,
            0,
        )
        self.combo_gold_thickness.SetSelection(0)
        fgSizer25.Add(self.combo_gold_thickness, 0, wx.ALL | wx.EXPAND, 5)

        labelProcessInfo.Add(fgSizer25, 0, wx.EXPAND, 5)

        self.SetSizer(labelProcessInfo)
        self.Layout()
        labelProcessInfo.Fit(self)

    def __del__(self):
        pass
