# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.0.0-0-g0efcecf)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

BOX_SIZE_SETTING = 2000

###########################################################################
## Class UiSmtBaseInfo
###########################################################################

class UiSmtBaseInfo ( wx.Panel ):

	def __init__( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.TAB_TRAVERSAL, name = wx.EmptyString ):
		wx.Panel.__init__ ( self, parent, id = id, pos = pos, size = size, style = style, name = name )

		sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, _(u"Base Info") ), wx.VERTICAL )

		fgSizer2 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer2.AddGrowableCol( 1 )
		fgSizer2.SetFlexibleDirection( wx.BOTH )
		fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.application_sphere_label = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, _(u"Application Sphere"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.application_sphere_label.Wrap( -1 )

		fgSizer2.Add( self.application_sphere_label, 0, wx.ALL, 5 )

		application_sphereChoices = []
		self.application_sphere = wx.Choice( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, application_sphereChoices, 0 )
		self.application_sphere.SetSelection( 0 )
		fgSizer2.Add( self.application_sphere, 0, wx.ALL|wx.EXPAND, 5 )

		self.is_pcb_soft_board_label = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, _(u"PCB Board Type"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.is_pcb_soft_board_label.Wrap( -1 )

		fgSizer2.Add( self.is_pcb_soft_board_label, 0, wx.ALL, 5 )

		is_pcb_soft_boardChoices = []
		self.is_pcb_soft_board = wx.Choice( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, is_pcb_soft_boardChoices, 0 )
		self.is_pcb_soft_board.SetSelection( 0 )
		fgSizer2.Add( self.is_pcb_soft_board, 0, wx.ALL|wx.EXPAND, 5 )

		self.single_or_double_technique_label = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, _(u"Single/Double Side"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.single_or_double_technique_label.Wrap( -1 )

		fgSizer2.Add( self.single_or_double_technique_label, 0, wx.ALL, 5 )

		single_or_double_techniqueChoices = []
		self.single_or_double_technique = wx.Choice( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, single_or_double_techniqueChoices, 0 )
		self.single_or_double_technique.SetSelection( 0 )
		fgSizer2.Add( self.single_or_double_technique, 0, wx.ALL|wx.EXPAND, 5 )

		self.custom_pcb_board_label = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, _(u"Custom PCB Board"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.custom_pcb_board_label.Wrap( -1 )

		fgSizer2.Add( self.custom_pcb_board_label, 0, wx.ALL, 5 )

		custom_pcb_boardChoices = []
		self.custom_pcb_board = wx.Choice( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, custom_pcb_boardChoices, 0 )
		self.custom_pcb_board.SetSelection( 0 )
		fgSizer2.Add( self.custom_pcb_board, 0, wx.ALL|wx.EXPAND, 5 )

		self.bom_purchase_label = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, _(u"BOM Material Purchase"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.bom_purchase_label.Wrap( -1 )

		fgSizer2.Add( self.bom_purchase_label, 0, wx.ALL, 5 )

		bom_purchaseChoices = []
		self.bom_purchase = wx.Choice( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, bom_purchaseChoices, 0 )
		self.bom_purchase.SetSelection( 0 )
		fgSizer2.Add( self.bom_purchase, 0, wx.ALL|wx.EXPAND, 5 )


		sbSizer2.Add( fgSizer2, 0, wx.EXPAND, 5 )

		fgSizer3 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer3.AddGrowableCol( 1 )
		fgSizer3.SetFlexibleDirection( wx.HORIZONTAL )
		fgSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.label_quantity = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, _(u"Qty(Single)"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.label_quantity.Wrap( -1 )

		self.label_quantity.SetToolTip( _(u"The total number of single pieces to be produced, the number of non-assembled plates") )

		fgSizer3.Add( self.label_quantity, 0, wx.ALL, 5 )

		fgSizer6 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer6.AddGrowableCol( 0 )
		fgSizer6.SetFlexibleDirection( wx.BOTH )
		fgSizer6.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.combo_number = wx.TextCtrl( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer6.Add( self.combo_number, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText10 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, _(u"pcs"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10.Wrap( -1 )

		fgSizer6.Add( self.m_staticText10, 0, wx.ALL, 5 )


		fgSizer3.Add( fgSizer6, 1, wx.EXPAND, 5 )


		sbSizer2.Add( fgSizer3, 0, wx.EXPAND, 5 )

		bSizer2 = wx.BoxSizer( wx.VERTICAL )

		box_piece_or_panel_size = wx.StaticBoxSizer( wx.StaticBox( sbSizer2.GetStaticBox(), BOX_SIZE_SETTING, _(u"Size (Single)") ), wx.VERTICAL )

		fgSizer41 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer41.AddGrowableCol( 1 )
		fgSizer41.SetFlexibleDirection( wx.BOTH )
		fgSizer41.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText82 = wx.StaticText( box_piece_or_panel_size.GetStaticBox(), wx.ID_ANY, _(u"X:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText82.Wrap( -1 )

		fgSizer41.Add( self.m_staticText82, 0, wx.ALL, 5 )

		fgSizer62 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer62.AddGrowableCol( 0 )
		fgSizer62.SetFlexibleDirection( wx.BOTH )
		fgSizer62.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.edit_size_x = wx.TextCtrl( box_piece_or_panel_size.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer62.Add( self.edit_size_x, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText102 = wx.StaticText( box_piece_or_panel_size.GetStaticBox(), wx.ID_ANY, _(u"mm"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText102.Wrap( -1 )

		fgSizer62.Add( self.m_staticText102, 0, wx.ALL, 5 )


		fgSizer41.Add( fgSizer62, 1, wx.EXPAND, 5 )

		self.m_staticText811 = wx.StaticText( box_piece_or_panel_size.GetStaticBox(), wx.ID_ANY, _(u"Y:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText811.Wrap( -1 )

		fgSizer41.Add( self.m_staticText811, 0, wx.ALL, 5 )

		fgSizer611 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer611.AddGrowableCol( 0 )
		fgSizer611.SetFlexibleDirection( wx.BOTH )
		fgSizer611.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.edit_size_y = wx.TextCtrl( box_piece_or_panel_size.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer611.Add( self.edit_size_y, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText1011 = wx.StaticText( box_piece_or_panel_size.GetStaticBox(), wx.ID_ANY, _(u"mm"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1011.Wrap( -1 )

		fgSizer611.Add( self.m_staticText1011, 0, wx.ALL, 5 )


		fgSizer41.Add( fgSizer611, 1, wx.EXPAND, 5 )


		box_piece_or_panel_size.Add( fgSizer41, 1, wx.EXPAND, 5 )


		bSizer2.Add( box_piece_or_panel_size, 0, wx.EXPAND, 5 )


		sbSizer2.Add( bSizer2, 0, wx.EXPAND, 5 )


		self.SetSizer( sbSizer2 )
		self.Layout()
		sbSizer2.Fit( self )

	def __del__( self ):
		pass

