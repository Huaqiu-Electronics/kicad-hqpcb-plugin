# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.0.0-0-g0efcecf)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.dataview
from kicad_amf_plugin.utils.platebtn import PlateButton ,PB_STYLE_GRADIENT
from kicad_amf_plugin.utils.platebtn import PlateButton ,PB_STYLE_GRADIENT,PB_STYLE_SQUARE

###########################################################################
## Class UiSummaryPanel
###########################################################################

class UiSummaryPanel ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 319,385 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		bSizer3 = wx.BoxSizer( wx.VERTICAL )

		self.m_panel10 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,10 ), wx.TAB_TRAVERSAL )
		bSizer3.Add( self.m_panel10, 0, wx.EXPAND |wx.ALL, 5 )


		bSizer1.Add( bSizer3, 0, wx.EXPAND, 5 )

		self.splitter_detail_summary = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_LIVE_UPDATE )
		self.splitter_detail_summary.Bind( wx.EVT_IDLE, self.splitter_detail_summaryOnIdle )

		self.m_panel7 = wx.Panel( self.splitter_detail_summary, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer13 = wx.BoxSizer( wx.VERTICAL )

		self.switch_smt_splitter = wx.SplitterWindow( self.m_panel7, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
		self.switch_smt_splitter.Bind( wx.EVT_IDLE, self.switch_smt_splitterOnIdle )

		self.switch_smt_panel = wx.Panel( self.switch_smt_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer10 = wx.BoxSizer( wx.VERTICAL )

		sbSizer7 = wx.StaticBoxSizer( wx.StaticBox( self.switch_smt_panel, wx.ID_ANY, _(u"BOM View") ), wx.VERTICAL )

		self.list_bom_view = wx.dataview.DataViewListCtrl( sbSizer7.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.DV_ROW_LINES|wx.dataview.DV_VERT_RULES )
		sbSizer7.Add( self.list_bom_view, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer10.Add( sbSizer7, 2, wx.EXPAND, 5 )

		self.btn_bom_match=PlateButton(self.switch_smt_panel,bmp= wx.Bitmap( self.GetImagePath("bom_match.png" ),wx.BITMAP_TYPE_ANY ),style=PB_STYLE_GRADIENT ,label=_("BOM Match"))
		bSizer10.Add( self.btn_bom_match, 0, wx.ALL|wx.EXPAND, 5 )


		self.switch_smt_panel.SetSizer( bSizer10 )
		self.switch_smt_panel.Layout()
		bSizer10.Fit( self.switch_smt_panel )
		self.m_panel9 = wx.Panel( self.switch_smt_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel9, wx.ID_ANY, _(u"Cost Detail") ), wx.VERTICAL )

		self.list_price_detail = wx.dataview.DataViewCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.DV_ROW_LINES|wx.dataview.DV_VERT_RULES )
		sbSizer1.Add( self.list_price_detail, 1, wx.ALL|wx.EXPAND, 5 )


		self.m_panel9.SetSizer( sbSizer1 )
		self.m_panel9.Layout()
		sbSizer1.Fit( self.m_panel9 )
		self.switch_smt_splitter.SplitHorizontally( self.switch_smt_panel, self.m_panel9, 0 )
		bSizer13.Add( self.switch_smt_splitter, 1, wx.EXPAND, 0 )


		self.m_panel7.SetSizer( bSizer13 )
		self.m_panel7.Layout()
		bSizer13.Fit( self.m_panel7 )
		self.switch_amf_panel = wx.Panel( self.splitter_detail_summary, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer101 = wx.BoxSizer( wx.VERTICAL )

		sbSizer41 = wx.StaticBoxSizer( wx.StaticBox( self.switch_amf_panel, wx.ID_ANY, _(u"Order Summary") ), wx.VERTICAL )

		self.list_order_summary = wx.dataview.DataViewCtrl( sbSizer41.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.DV_ROW_LINES|wx.dataview.DV_VERT_RULES )
		sbSizer41.Add( self.list_order_summary, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer101.Add( sbSizer41, 1, wx.EXPAND, 5 )

		self.show_hidden_text = wx.Panel( self.switch_amf_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sbSizer5 = wx.StaticBoxSizer( wx.StaticBox( self.show_hidden_text, wx.ID_ANY, _(u"Tip") ), wx.VERTICAL )

		self.m_staticText1 = wx.StaticText( sbSizer5.GetStaticBox(), wx.ID_ANY, _(u"Factors that affect the price : Layer,  Min Trace/Space Outer, Min Pilled Hole "), wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ST_ELLIPSIZE_MIDDLE )
		self.m_staticText1.Wrap( 310 )

		sbSizer5.Add( self.m_staticText1, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.min_trace_outer_text = wx.StaticText( sbSizer5.GetStaticBox(), wx.ID_ANY, _(u"Min Trace/Space Outer(Recommand) : 6mil--10mil"), wx.DefaultPosition, wx.DefaultSize, wx.ST_ELLIPSIZE_MIDDLE )
		self.min_trace_outer_text.Wrap( -1 )

		self.min_trace_outer_text.Hide()

		sbSizer5.Add( self.min_trace_outer_text, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.board_type_text = wx.StaticText( sbSizer5.GetStaticBox(), wx.ID_ANY, _(u"Board Type (Recommand) : Single Piece"), wx.DefaultPosition, wx.DefaultSize, wx.ST_ELLIPSIZE_MIDDLE )
		self.board_type_text.Wrap( -1 )

		self.board_type_text.Hide()

		sbSizer5.Add( self.board_type_text, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.flnsihed_copper_text = wx.StaticText( sbSizer5.GetStaticBox(), wx.ID_ANY, _(u"Flnsihed Copper Weight (Best Price) : 1zo"), wx.DefaultPosition, wx.DefaultSize, wx.ST_ELLIPSIZE_MIDDLE )
		self.flnsihed_copper_text.Wrap( -1 )

		self.flnsihed_copper_text.Hide()

		sbSizer5.Add( self.flnsihed_copper_text, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		self.solder_mask_text = wx.StaticText( sbSizer5.GetStaticBox(), wx.ID_ANY, _(u"Solder Mask Color (Best Price) : Green"), wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ST_ELLIPSIZE_MIDDLE )
		self.solder_mask_text.Wrap( -1 )

		self.solder_mask_text.Hide()

		sbSizer5.Add( self.solder_mask_text, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


		self.show_hidden_text.SetSizer( sbSizer5 )
		self.show_hidden_text.Layout()
		sbSizer5.Fit( self.show_hidden_text )
		bSizer101.Add( self.show_hidden_text, 0, wx.EXPAND |wx.ALL, 5 )


		self.switch_amf_panel.SetSizer( bSizer101 )
		self.switch_amf_panel.Layout()
		bSizer101.Fit( self.switch_amf_panel )
		self.splitter_detail_summary.SplitHorizontally( self.m_panel7, self.switch_amf_panel, 0 )
		bSizer1.Add( self.splitter_detail_summary, 1, wx.EXPAND, 5 )

		bSizer31 = wx.BoxSizer( wx.VERTICAL )

		self.btn_update_price=PlateButton(self,bmp= wx.Bitmap( self.GetImagePath("query.png" ),wx.BITMAP_TYPE_ANY ),style=PB_STYLE_GRADIENT ,label=_("Update Price"))
		bSizer31.Add( self.btn_update_price, 1, wx.ALL|wx.EXPAND, 5 )

		self.btn_place_order=PlateButton(self,bmp= wx.Bitmap( self.GetImagePath("cart.png" ),wx.BITMAP_TYPE_ANY ),style=PB_STYLE_GRADIENT ,label=_("Add to Cart"))
		bSizer31.Add( self.btn_place_order, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer1.Add( bSizer31, 0, wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

	def __del__( self ):
		pass

	def splitter_detail_summaryOnIdle( self, event ):
		self.splitter_detail_summary.SetSashPosition( 0 )
		self.splitter_detail_summary.Unbind( wx.EVT_IDLE )

	def switch_smt_splitterOnIdle( self, event ):
		self.switch_smt_splitter.SetSashPosition( 0 )
		self.switch_smt_splitter.Unbind( wx.EVT_IDLE )

	# Virtual image path resolution method. Override this in your derived class.
	def GetImagePath( self, bitmap_path ):
		return bitmap_path


###########################################################################
## Class MyPanel2
###########################################################################

class MyPanel2 ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer11 = wx.BoxSizer( wx.VERTICAL )

		self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer7 = wx.BoxSizer( wx.VERTICAL )


		self.m_panel1.SetSizer( bSizer7 )
		self.m_panel1.Layout()
		bSizer7.Fit( self.m_panel1 )
		bSizer11.Add( self.m_panel1, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizer( bSizer11 )
		self.Layout()

	def __del__( self ):
		pass

	# Virtual image path resolution method. Override this in your derived class.
	def GetImagePath( self, bitmap_path ):
		return bitmap_path


