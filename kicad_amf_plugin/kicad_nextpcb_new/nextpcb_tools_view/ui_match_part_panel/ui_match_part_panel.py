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
## Class UiMatchPartPanel
###########################################################################

class UiMatchPartPanel ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 438,235 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer3 = wx.BoxSizer( wx.VERTICAL )

		bSizer1 = wx.BoxSizer( wx.HORIZONTAL )

		self.select_part_button = wx.Button( self, wx.ID_ANY, _(" Manual Match "), wx.Point( 0,0 ), wx.DefaultSize, 0 )
		bSizer1.Add( self.select_part_button, 0, wx.ALL, 5 )

		self.remove_part_button = wx.Button( self, wx.ID_ANY, _(" Remove Assigned MPN ") , wx.DefaultPosition, wx.DefaultSize, 0 )
		self.remove_part_button.SetToolTip( _("Remove Assigned MPN ") )

		bSizer1.Add( self.remove_part_button, 0, wx.ALL, 5 )


		bSizer1.Add( ( 0, 0), 2, wx.EXPAND, 5 )

		self.export_csv = wx.Button( self, wx.ID_ANY, _(" Epxort... "), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1.Add( self.export_csv, 0, wx.ALL, 5 )

		bSizer2 = wx.BoxSizer( wx.VERTICAL )


		bSizer1.Add( bSizer2, 1, wx.EXPAND, 5 )


		bSizer3.Add( bSizer1, 0, wx.EXPAND, 5 )


		self.SetSizer( bSizer3 )
		self.Layout()

	def __del__( self ):
		pass


















