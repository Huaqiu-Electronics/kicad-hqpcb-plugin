import wx
from kicad_amf_plugin.nextpcb_smt.pcb_fabrication.base.base_smt_view import BaseSmtView
from kicad_amf_plugin.nextpcb_smt.pcb_fabrication.personalized.personalized_smt_view import PersonalizedSmtView
from kicad_amf_plugin.nextpcb_smt.pcb_fabrication.process.process_smt_view import ProcessSmtView
from kicad_amf_plugin.nextpcb_smt.pcb_fabrication.special_process.special_process_smt_view import SpecialProcessSmtView
from kicad_amf_plugin.nextpcb_smt.pcb_assembly.region_select.region_select_view import RegionSelectView
from kicad_amf_plugin.nextpcb_smt.pcb_assembly.order_summary.order_summary_view import OrderSummaryView

from enum import Enum

from kicad_amf_plugin.kicad.board_manager import BoardManager
from kicad_amf_plugin.utils.form_panel_base import FormKind, FormPanelBase


class PCBFormPart(Enum):
    BASE_INFO = 0
    PROCESS_INFO = 1
    SPECIAL_PROCESS = 2
    PERSONALIZED = 3


PCB_PANEL_CTORS = {
    PCBFormPart.BASE_INFO: BaseSmtView,
    PCBFormPart.PROCESS_INFO: ProcessSmtView,
    PCBFormPart.SPECIAL_PROCESS: SpecialProcessSmtView,
    PCBFormPart.PERSONALIZED: PersonalizedSmtView,
}


class SMTMainPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)

        self._board_manager = BoardManager
        self._pcb_form_parts: "dict[PCBFormPart, FormPanelBase]" = {} 

        # ---------------------------------------------------------------------
        # ---------------------------- smt SplitterWindow ---------------------
        # ---------------------------------------------------------------------
        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        main_sizer = wx.BoxSizer( wx.HORIZONTAL )

        self.smt_splitter = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
        self.smt_splitter.Bind( wx.EVT_IDLE, self.smt_splitterOnIdle )
        self.smt_scrolledWindow = wx.ScrolledWindow( self.smt_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
        self.smt_scrolledWindow.SetScrollRate( 5, 5 )
        
        lay_pcb_fab_panel = wx.BoxSizer(wx.VERTICAL)
        for i in PCB_PANEL_CTORS:
            view = PCB_PANEL_CTORS[i](self.smt_scrolledWindow, self._board_manager)
            self._pcb_form_parts[i] = view
            lay_pcb_fab_panel.Add(view, 0, wx.ALL | wx.EXPAND, 5)
        self.smt_scrolledWindow.SetSizer(lay_pcb_fab_panel)
        self.smt_scrolledWindow.Layout()
        
        # ---------------------------------------------------------------------
        # ---------------------------- smt Panel ------------------------------
        # ---------------------------------------------------------------------
        
        self.smt_right_panel = wx.Panel( self.smt_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        right_sizer = wx.BoxSizer( wx.VERTICAL )
        region_select_view = RegionSelectView( self.smt_right_panel )
        order_summary_view = OrderSummaryView( self.smt_right_panel )
        
        right_sizer.Add(region_select_view, 0, wx.EXPAND | wx.ALL, 0)
        right_sizer.Add(order_summary_view, 2, wx.EXPAND | wx.ALL, 0)
        
        self.smt_right_panel.SetSizer( right_sizer )
        self.smt_splitter.SplitVertically( self.smt_scrolledWindow, self.smt_right_panel, 0 )
        self.smt_splitter.SetSashPosition(400)
        main_sizer.Add( self.smt_splitter, 1, wx.EXPAND, 0 )
        self.SetSizer( main_sizer )
        self.Layout()
        self.Centre( wx.BOTH )


    def __del__( self ):
        pass

    def smt_splitterOnIdle( self, event ):
        self.smt_splitter.SetSashPosition( 0 )
        self.smt_splitter.Unbind( wx.EVT_IDLE )
        