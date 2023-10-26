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
## Class UiSpecialProcess
###########################################################################


class UiSpecialProcess(wx.Panel):
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
            wx.StaticBox(self, wx.ID_ANY, _("Special Process")), wx.VERTICAL
        )

        fgSizer25 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer25.AddGrowableCol(1)
        fgSizer25.SetFlexibleDirection(wx.BOTH)
        fgSizer25.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_staticText401 = wx.StaticText(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            _("Impedance"),
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_staticText401.Wrap(-1)

        fgSizer25.Add(self.m_staticText401, 0, wx.ALL, 5)

        combo_impedanceChoices = []
        self.combo_impedance = wx.Choice(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            combo_impedanceChoices,
            0,
        )
        self.combo_impedance.SetSelection(0)
        fgSizer25.Add(self.combo_impedance, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText4011 = wx.StaticText(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            _("Beveling of G/F"),
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_staticText4011.Wrap(-1)

        fgSizer25.Add(self.m_staticText4011, 0, wx.ALL, 5)

        combo_goldFingerChoices = []
        self.combo_goldFinger = wx.Choice(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            combo_goldFingerChoices,
            0,
        )
        self.combo_goldFinger.SetSelection(0)
        fgSizer25.Add(self.combo_goldFinger, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText40111 = wx.StaticText(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            _("Plated Half Holes"),
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_staticText40111.Wrap(-1)

        fgSizer25.Add(self.m_staticText40111, 0, wx.ALL, 5)

        combo_halfHoleChoices = []
        self.combo_halfHole = wx.Choice(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            combo_halfHoleChoices,
            0,
        )
        self.combo_halfHole.SetSelection(0)
        fgSizer25.Add(self.combo_halfHole, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText401111 = wx.StaticText(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            _("Pad Hole"),
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_staticText401111.Wrap(-1)

        fgSizer25.Add(self.m_staticText401111, 0, wx.ALL, 5)

        combo_pad_holeChoices = []
        self.combo_pad_hole = wx.Choice(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            combo_pad_holeChoices,
            0,
        )
        self.combo_pad_hole.SetSelection(0)
        fgSizer25.Add(self.combo_pad_hole, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText4011111 = wx.StaticText(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            _("HDI(Buried/blind vais)"),
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_staticText4011111.Wrap(-1)

        fgSizer25.Add(self.m_staticText4011111, 0, wx.ALL, 5)

        combo_blind_viaChoices = []
        self.combo_blind_via = wx.Choice(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            combo_blind_viaChoices,
            0,
        )
        self.combo_blind_via.SetSelection(0)
        fgSizer25.Add(self.combo_blind_via, 0, wx.ALL | wx.EXPAND, 5)

        self.label_hdi = wx.StaticText(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            _("HDI Structure"),
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.label_hdi.Wrap(-1)

        fgSizer25.Add(self.label_hdi, 0, wx.ALL, 5)

        combo_hdi_structureChoices = []
        self.combo_hdi_structure = wx.Choice(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            combo_hdi_structureChoices,
            0,
        )
        self.combo_hdi_structure.SetSelection(0)
        fgSizer25.Add(self.combo_hdi_structure, 0, wx.ALL | wx.EXPAND, 5)

        self.label_stackup = wx.StaticText(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            _("Stack up"),
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.label_stackup.Wrap(-1)

        fgSizer25.Add(self.label_stackup, 0, wx.ALL, 5)

        combo_stackupChoices = []
        self.combo_stackup = wx.Choice(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            combo_stackupChoices,
            0,
        )
        self.combo_stackup.SetSelection(0)
        fgSizer25.Add(self.combo_stackup, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText8 = wx.StaticText(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            _("Metallized Sides Count"),
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_staticText8.Wrap(-1)

        fgSizer25.Add(self.m_staticText8, 0, wx.ALL, 5)

        combo_baobianChoices = []
        self.combo_baobian = wx.Choice(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            combo_baobianChoices,
            0,
        )
        self.combo_baobian.SetSelection(0)
        fgSizer25.Add(self.combo_baobian, 0, wx.ALL | wx.EXPAND, 5)

        labelProcessInfo.Add(fgSizer25, 0, wx.EXPAND, 5)

        self.SetSizer(labelProcessInfo)
        self.Layout()
        labelProcessInfo.Fit(self)

    def __del__(self):
        pass
