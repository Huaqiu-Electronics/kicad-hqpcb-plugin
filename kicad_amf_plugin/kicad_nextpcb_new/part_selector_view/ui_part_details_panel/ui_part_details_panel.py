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

###########################################################################
## Class UiPartDetailsPanel
###########################################################################

class UiPartDetailsPanel ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		sbSizer6 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, _("Part Details") ), wx.VERTICAL )

		self.m_scrolledWindow4 = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.HSCROLL|wx.VSCROLL )
		self.m_scrolledWindow4.SetScrollRate( 5, 5 )
		bSizer11 = wx.BoxSizer( wx.VERTICAL )

		sbSizer3 = wx.StaticBoxSizer( wx.StaticBox( self.m_scrolledWindow4, wx.ID_ANY, _("Description") ), wx.VERTICAL )

		self.data_list = wx.dataview.DataViewListCtrl( sbSizer3.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer3.Add( self.data_list, 1, wx.EXPAND, 5 )


		bSizer11.Add( sbSizer3, 1, wx.EXPAND, 5 )

		sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self.m_scrolledWindow4, wx.ID_ANY, _("Picture") ), wx.VERTICAL )

		self.part_image = wx.StaticBitmap( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.part_image.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNSHADOW ) )
		self.part_image.SetBackgroundColour( wx.Colour( 255, 255, 255 ) )

		sbSizer2.Add( self.part_image, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer11.Add( sbSizer2, 1, wx.EXPAND, 5 )


		self.m_scrolledWindow4.SetSizer( bSizer11 )
		self.m_scrolledWindow4.Layout()
		bSizer11.Fit( self.m_scrolledWindow4 )
		sbSizer6.Add( self.m_scrolledWindow4, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizer( sbSizer6 )
		self.Layout()
		sbSizer6.Fit( self )

	def __del__( self ):
		pass


