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
## Class UiProcessInfo
###########################################################################

class UiProcessInfo ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		labelProcessInfo = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, _("Process info") ), wx.VERTICAL )

		fgSizer25 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer25.AddGrowableCol( 1 )
		fgSizer25.SetFlexibleDirection( wx.BOTH )
		fgSizer25.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.bom_material_type_label = wx.StaticText( labelProcessInfo.GetStaticBox(), wx.ID_ANY, _("BOM Material Type"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.bom_material_type_label.Wrap( -1 )

		fgSizer25.Add( self.bom_material_type_label, 0, wx.ALL, 5 )

		self.bom_material_type_number = wx.TextCtrl( labelProcessInfo.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer25.Add( self.bom_material_type_number, 0, wx.ALL|wx.EXPAND, 5 )

		self.patch_pad_number_label = wx.StaticText( labelProcessInfo.GetStaticBox(), wx.ID_ANY, _("Patch Pad Number"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.patch_pad_number_label.Wrap( -1 )

		fgSizer25.Add( self.patch_pad_number_label, 0, wx.ALL, 5 )

		self.patch_pad_number = wx.TextCtrl( labelProcessInfo.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer25.Add( self.patch_pad_number, 0, wx.ALL|wx.EXPAND, 5 )

		self.is_plug_label = wx.StaticText( labelProcessInfo.GetStaticBox(), wx.ID_ANY, _("Welding Plugin"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.is_plug_label.Wrap( -1 )

		fgSizer25.Add( self.is_plug_label, 0, wx.ALL, 5 )

		is_plugChoices = []
		self.is_plug = wx.Choice( labelProcessInfo.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, is_plugChoices, 0 )
		self.is_plug.SetSelection( 0 )
		fgSizer25.Add( self.is_plug, 0, wx.ALL|wx.EXPAND, 5 )

		self.plug_number_label = wx.StaticText( labelProcessInfo.GetStaticBox(), wx.ID_ANY, _("Single Plugin Points"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.plug_number_label.Wrap( -1 )

		fgSizer25.Add( self.plug_number_label, 0, wx.ALL, 5 )

		self.plug_number = wx.TextCtrl( labelProcessInfo.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer25.Add( self.plug_number, 0, wx.ALL|wx.EXPAND, 5 )

		self.steel_type_label = wx.StaticText( labelProcessInfo.GetStaticBox(), wx.ID_ANY, _("Steel Mesh"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.steel_type_label.Wrap( -1 )

		fgSizer25.Add( self.steel_type_label, 0, wx.ALL, 5 )

		steel_typeChoices = []
		self.steel_type = wx.Choice( labelProcessInfo.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, steel_typeChoices, 0 )
		self.steel_type.SetSelection( 0 )
		fgSizer25.Add( self.steel_type, 0, wx.ALL|wx.EXPAND, 5 )

		self.is_steel_follow_delivery_label = wx.StaticText( labelProcessInfo.GetStaticBox(), wx.ID_ANY, _("Steel Follow Delivery"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.is_steel_follow_delivery_label.Wrap( -1 )

		fgSizer25.Add( self.is_steel_follow_delivery_label, 0, wx.ALL, 5 )

		is_steel_follow_deliveryChoices = []
		self.is_steel_follow_delivery = wx.Choice( labelProcessInfo.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, is_steel_follow_deliveryChoices, 0 )
		self.is_steel_follow_delivery.SetSelection( 0 )
		fgSizer25.Add( self.is_steel_follow_delivery, 0, wx.ALL|wx.EXPAND, 5 )


		labelProcessInfo.Add( fgSizer25, 0, wx.EXPAND, 5 )


		self.SetSizer( labelProcessInfo )
		self.Layout()
		labelProcessInfo.Fit( self )

	def __del__( self ):
		pass



