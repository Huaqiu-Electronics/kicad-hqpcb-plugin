# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.0.0-0-g0efcecf)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class UiRegionSelect
###########################################################################

class UiRegionSelect ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,65 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		right_main_sizer = wx.BoxSizer( wx.VERTICAL )

		sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Preference" ), wx.HORIZONTAL )

		self.m_staticText2 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Website", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )

		sbSizer2.Add( self.m_staticText2, 0, wx.ALL, 8 )

		choice_order_regionChoices = []
		self.choice_order_region = wx.Choice( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, choice_order_regionChoices, 0 )
		self.choice_order_region.SetSelection( 0 )
		sbSizer2.Add( self.choice_order_region, 0, wx.ALL, 5 )


		right_main_sizer.Add( sbSizer2, 0, wx.EXPAND, 5 )


		self.SetSizer( right_main_sizer )
		self.Layout()

	def __del__( self ):
		pass
