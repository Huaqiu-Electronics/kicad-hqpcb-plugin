# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b3)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.dataview

###########################################################################
## Class UiImportListPanel
###########################################################################

class UiImportListPanel ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 761,458 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		bSizer2 = wx.BoxSizer( wx.VERTICAL )

		bSizer1 = wx.BoxSizer( wx.HORIZONTAL )


		bSizer1.Add( ( 10, 0), 0, wx.EXPAND, 5 )

		self.import_mapping = wx.Button( self, wx.ID_ANY, u"Import", wx.DefaultPosition, wx.Size( 120,-1 ), 0 )
		bSizer1.Add( self.import_mapping, 0, wx.ALL, 5 )


		bSizer1.Add( ( 20, 0), 0, wx.EXPAND, 5 )

		self.export_mapping = wx.Button( self, wx.ID_ANY, u"Export", wx.DefaultPosition, wx.Size( 120,-1 ), 0 )
		bSizer1.Add( self.export_mapping, 0, wx.ALL, 5 )


		bSizer1.Add( ( 20, 0), 0, wx.EXPAND, 5 )

		self.select_part_button = wx.Button( self, wx.ID_ANY, u" Manual Match ", wx.DefaultPosition, wx.Size( 120,-1 ), 0 )
		bSizer1.Add( self.select_part_button, 0, wx.ALL, 5 )


		bSizer1.Add( ( 20, 0), 0, wx.EXPAND, 5 )

		self.remove_part_button = wx.Button( self, wx.ID_ANY, u" Remove Assigned MPN ", wx.DefaultPosition, wx.Size( 150,-1 ), 0 )
		bSizer1.Add( self.remove_part_button, 0, wx.ALL, 5 )


		bSizer2.Add( bSizer1, 0, wx.ALL|wx.EXPAND, 5 )

		bSizer7 = wx.BoxSizer( wx.VERTICAL )

		self.show_list = wx.dataview.DataViewListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.show_list, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer2.Add( bSizer7, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer2 )
		self.Layout()

	def __del__( self ):
		pass