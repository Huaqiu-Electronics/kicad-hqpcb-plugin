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

import gettext
_ = gettext.gettext

###########################################################################
## Class UiOrderPanel
###########################################################################

class UiOrderPanel ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 406,341 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, _(u"PCBA Qty"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )

		bSizer9.Add( self.m_staticText2, 0, wx.ALL, 10 )

		self.m_textCtrl1 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer9.Add( self.m_textCtrl1, 1, wx.ALL, 5 )


		bSizer1.Add( bSizer9, 0, wx.EXPAND, 5 )

		self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel1, wx.ID_ANY, _(u"BOM view") ), wx.VERTICAL )

		self.list_bom_template = wx.dataview.DataViewCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.DV_ROW_LINES|wx.dataview.DV_VERT_RULES )
		sbSizer1.Add( self.list_bom_template, 3, wx.ALL|wx.EXPAND, 0 )


		self.m_panel1.SetSizer( sbSizer1 )
		self.m_panel1.Layout()
		sbSizer1.Fit( self.m_panel1 )
		bSizer1.Add( self.m_panel1, 2, wx.EXPAND |wx.ALL, 0 )

		bSizer311 = wx.BoxSizer( wx.VERTICAL )

		self.btn_bom_match=PlateButton(self,bmp= wx.Bitmap( self.GetImagePath("bom_match.png" ),wx.BITMAP_TYPE_ANY ),style=PB_STYLE_GRADIENT ,label=_("BOM Match"))
		bSizer311.Add( self.btn_bom_match, 0, wx.ALL|wx.EXPAND, 5 )


		bSizer1.Add( bSizer311, 0, wx.EXPAND, 5 )

		self.m_panel11 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		sbSizer11 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel11, wx.ID_ANY, _(u"Cost detail") ), wx.VERTICAL )

		self.list_price_detail = wx.dataview.DataViewCtrl( sbSizer11.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.DV_ROW_LINES|wx.dataview.DV_VERT_RULES )
		sbSizer11.Add( self.list_price_detail, 1, wx.ALL|wx.EXPAND, 0 )


		self.m_panel11.SetSizer( sbSizer11 )
		self.m_panel11.Layout()
		sbSizer11.Fit( self.m_panel11 )
		bSizer1.Add( self.m_panel11, 1, wx.EXPAND |wx.ALL, 0 )

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

	# Virtual image path resolution method. Override this in your derived class.
	def GetImagePath( self, bitmap_path ):
		return bitmap_path