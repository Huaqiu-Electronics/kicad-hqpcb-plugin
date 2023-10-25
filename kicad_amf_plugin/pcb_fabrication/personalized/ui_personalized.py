# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b3)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

BOX_SP_REQUEST = 1030

###########################################################################
## Class UiPersonalizedService
###########################################################################


class UiPersonalizedService(wx.Panel):
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
            wx.StaticBox(self, wx.ID_ANY, _("Personalized Service")), wx.VERTICAL
        )

        fgSizer25 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer25.AddGrowableCol(1)
        fgSizer25.SetFlexibleDirection(wx.BOTH)
        fgSizer25.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.label_electric_test = wx.StaticText(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            _("Electrical Test"),
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.label_electric_test.Wrap(-1)

        fgSizer25.Add(self.label_electric_test, 0, wx.ALL, 5)

        comb_test_methodChoices = []
        self.comb_test_method = wx.Choice(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            comb_test_methodChoices,
            0,
        )
        self.comb_test_method.SetSelection(0)
        fgSizer25.Add(self.comb_test_method, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText4011 = wx.StaticText(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            _("Approve Working Gerber"),
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_staticText4011.Wrap(-1)

        fgSizer25.Add(self.m_staticText4011, 0, wx.ALL, 5)

        comb_approve_gerberChoices = []
        self.comb_approve_gerber = wx.Choice(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            comb_approve_gerberChoices,
            0,
        )
        self.comb_approve_gerber.SetSelection(0)
        fgSizer25.Add(self.comb_approve_gerber, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText40111 = wx.StaticText(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            _("Delivery Report"),
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_staticText40111.Wrap(-1)

        fgSizer25.Add(self.m_staticText40111, 0, wx.ALL, 5)

        combo_microsection_reportChoices = []
        self.combo_microsection_report = wx.Choice(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            combo_microsection_reportChoices,
            0,
        )
        self.combo_microsection_report.SetSelection(0)
        fgSizer25.Add(self.combo_microsection_report, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText401111 = wx.StaticText(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            _("Microsection Analysis Report"),
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_staticText401111.Wrap(-1)

        fgSizer25.Add(self.m_staticText401111, 0, wx.ALL, 5)

        comb_delivery_reportChoices = []
        self.comb_delivery_report = wx.Choice(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            comb_delivery_reportChoices,
            0,
        )
        self.comb_delivery_report.SetSelection(0)
        fgSizer25.Add(self.comb_delivery_report, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText4011111 = wx.StaticText(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            _("Report Format"),
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_staticText4011111.Wrap(-1)

        fgSizer25.Add(self.m_staticText4011111, 0, wx.ALL, 5)

        comb_report_formatChoices = []
        self.comb_report_format = wx.Choice(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            comb_report_formatChoices,
            0,
        )
        self.comb_report_format.SetSelection(0)
        fgSizer25.Add(self.comb_report_format, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText40111111 = wx.StaticText(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            _("UL Mark"),
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_staticText40111111.Wrap(-1)

        fgSizer25.Add(self.m_staticText40111111, 0, wx.ALL, 5)

        comb_ul_markChoices = []
        self.comb_ul_mark = wx.Choice(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            comb_ul_markChoices,
            0,
        )
        self.comb_ul_mark.SetSelection(0)
        fgSizer25.Add(self.comb_ul_mark, 0, wx.ALL | wx.EXPAND, 5)

        self.label_stackup = wx.StaticText(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            _("Film"),
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.label_stackup.Wrap(-1)

        fgSizer25.Add(self.label_stackup, 0, wx.ALL, 5)

        comb_filmChoices = []
        self.comb_film = wx.Choice(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            comb_filmChoices,
            0,
        )
        self.comb_film.SetSelection(0)
        fgSizer25.Add(self.comb_film, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText8 = wx.StaticText(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            _("Cross Board"),
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_staticText8.Wrap(-1)

        fgSizer25.Add(self.m_staticText8, 0, wx.ALL, 5)

        combo_cross_boardChoices = []
        self.combo_cross_board = wx.Choice(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            combo_cross_boardChoices,
            0,
        )
        self.combo_cross_board.SetSelection(0)
        fgSizer25.Add(self.combo_cross_board, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText9 = wx.StaticText(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            _("Bulkhead Paper"),
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_staticText9.Wrap(-1)

        fgSizer25.Add(self.m_staticText9, 0, wx.ALL, 5)

        combo_paperChoices = []
        self.combo_paper = wx.Choice(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            combo_paperChoices,
            0,
        )
        self.combo_paper.SetSelection(0)
        fgSizer25.Add(self.combo_paper, 0, wx.ALL | wx.EXPAND, 5)

        self.m_staticText10 = wx.StaticText(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            _("User Stamp Process"),
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_staticText10.Wrap(-1)

        fgSizer25.Add(self.m_staticText10, 0, wx.ALL, 5)

        combo_user_stampChoices = []
        self.combo_user_stamp = wx.Choice(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            combo_user_stampChoices,
            0,
        )
        self.combo_user_stamp.SetSelection(0)
        fgSizer25.Add(self.combo_user_stamp, 0, wx.ALL | wx.EXPAND, 5)

        self.label_hq_pack = wx.StaticText(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            _("HQ Pack"),
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.label_hq_pack.Wrap(-1)

        fgSizer25.Add(self.label_hq_pack, 0, wx.ALL, 5)

        combo_hq_packChoices = []
        self.combo_hq_pack = wx.Choice(
            labelProcessInfo.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            combo_hq_packChoices,
            0,
        )
        self.combo_hq_pack.SetSelection(0)
        fgSizer25.Add(self.combo_hq_pack, 0, wx.ALL | wx.EXPAND, 5)

        labelProcessInfo.Add(fgSizer25, 0, wx.EXPAND, 5)

        sp_box = wx.StaticBoxSizer(
            wx.StaticBox(
                labelProcessInfo.GetStaticBox(), BOX_SP_REQUEST, _("Special Request")
            ),
            wx.VERTICAL,
        )

        self.edit_special_request = wx.TextCtrl(
            sp_box.GetStaticBox(),
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TE_MULTILINE,
        )
        self.edit_special_request.SetMinSize(wx.Size(-1, 60))

        sp_box.Add(self.edit_special_request, 1, wx.ALL | wx.EXPAND, 5)

        labelProcessInfo.Add(sp_box, 1, wx.EXPAND, 5)

        self.SetSizer(labelProcessInfo)
        self.Layout()
        labelProcessInfo.Fit(self)

    def __del__(self):
        pass
