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

import gettext
_ = gettext.gettext

###########################################################################
## Class AmfDialogBase
###########################################################################

class AmfDialogBase ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"HQ NextPCB Active Manufacturing"), pos = wx.DefaultPosition, size = wx.Size( 800, 700 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		m_mainSizer = wx.BoxSizer( wx.VERTICAL )

		m_topSizer = wx.BoxSizer( wx.HORIZONTAL )

		m_topLeftSizer = wx.BoxSizer( wx.VERTICAL )

		m_templateChoices = [ _(u"PCB Fabrication") ]
		self.m_template = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 300,-1 ), m_templateChoices, 0 )
		self.m_template.SetSelection( 0 )
		m_topLeftSizer.Add( self.m_template, 0, wx.EXPAND|wx.TOP, 5 )

		self.m_notebook = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 300,-1 ), 0 )
		self.m_panelFab = wx.ScrolledWindow( self.m_notebook, wx.ID_ANY, wx.DefaultPosition, wx.Size( 300,-1 ), wx.HSCROLL|wx.VSCROLL )
		self.m_panelFab.SetScrollRate( 10, 10 )
		m_panelFabSizer = wx.BoxSizer( wx.VERTICAL )

		m_fabBaseInfo = wx.StaticBoxSizer( wx.StaticBox( self.m_panelFab, wx.ID_ANY, _(u"Base Info") ), wx.VERTICAL )

		m_fabBaseInfoSizer = wx.GridBagSizer( 0, 0 )
		m_fabBaseInfoSizer.SetFlexibleDirection( wx.BOTH )
		m_fabBaseInfoSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_baseMaterialLabel = wx.StaticText( m_fabBaseInfo.GetStaticBox(), wx.ID_ANY, _(u"Material Type:"), wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.m_baseMaterialLabel.Wrap( -1 )

		self.m_baseMaterialLabel.SetToolTip( _(u"Non-conductive base material") )

		m_fabBaseInfoSizer.Add( self.m_baseMaterialLabel, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_baseMaterialCtrlChoices = [ _(u"FR-4") ]
		self.m_baseMaterialCtrl = wx.Choice( m_fabBaseInfo.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size( 100,-1 ), m_baseMaterialCtrlChoices, 0 )
		self.m_baseMaterialCtrl.SetSelection( 0 )
		m_fabBaseInfoSizer.Add( self.m_baseMaterialCtrl, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		self.m_layerCountLabel = wx.StaticText( m_fabBaseInfo.GetStaticBox(), wx.ID_ANY, _(u"Layer Count:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_layerCountLabel.Wrap( -1 )

		self.m_layerCountLabel.SetToolTip( _(u"Number of copper layers") )

		m_fabBaseInfoSizer.Add( self.m_layerCountLabel, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_layerCountCtrlChoices = [ _(u"1"), _(u"2"), _(u"4"), _(u"6"), _(u"8"), _(u"10"), _(u"12"), _(u"14"), _(u"16"), _(u"18"), _(u"20") ]
		self.m_layerCountCtrl = wx.Choice( m_fabBaseInfo.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size( 100,-1 ), m_layerCountCtrlChoices, 0 )
		self.m_layerCountCtrl.SetSelection( 1 )
		m_fabBaseInfoSizer.Add( self.m_layerCountCtrl, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		self.m_pcbPackaingLabel = wx.StaticText( m_fabBaseInfo.GetStaticBox(), wx.ID_ANY, _(u"Board Type:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_pcbPackaingLabel.Wrap( -1 )

		self.m_pcbPackaingLabel.SetToolTip( _(u"The finished PCB are by single or by panel") )

		m_fabBaseInfoSizer.Add( self.m_pcbPackaingLabel, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_pcbPackaingCtrlChoices = [ _(u"Single Piece"), _(u"Panel by Customer"), _(u"Panel by NextPCB") ]
		self.m_pcbPackaingCtrl = wx.Choice( m_fabBaseInfo.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size( 100,-1 ), m_pcbPackaingCtrlChoices, 0 )
		self.m_pcbPackaingCtrl.SetSelection( 0 )
		m_fabBaseInfoSizer.Add( self.m_pcbPackaingCtrl, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		self.m_panelizeRuleLbel = wx.StaticText( m_fabBaseInfo.GetStaticBox(), wx.ID_ANY, _(u"Panel Type:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panelizeRuleLbel.Wrap( -1 )

		m_fabBaseInfoSizer.Add( self.m_panelizeRuleLbel, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_panelizeXLabel = wx.StaticText( m_fabBaseInfo.GetStaticBox(), wx.ID_ANY, _(u"X:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panelizeXLabel.Wrap( -1 )

		m_fabBaseInfoSizer.Add( self.m_panelizeXLabel, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_RIGHT|wx.ALL, 5 )

		self.m_panelizeXCtrl = wx.TextCtrl( m_fabBaseInfo.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 100,-1 ), wx.TE_READONLY )
		self.m_panelizeXCtrl.SetMaxLength( 0 )
		m_fabBaseInfoSizer.Add( self.m_panelizeXCtrl, wx.GBPosition( 4, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_panelizeXUnit = wx.StaticText( m_fabBaseInfo.GetStaticBox(), wx.ID_ANY, _(u"pcs"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panelizeXUnit.Wrap( -1 )

		m_fabBaseInfoSizer.Add( self.m_panelizeXUnit, wx.GBPosition( 4, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_panelizeYCtrl = wx.TextCtrl( m_fabBaseInfo.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 100,-1 ), wx.TE_READONLY )
		self.m_panelizeYCtrl.SetMaxLength( 0 )
		m_fabBaseInfoSizer.Add( self.m_panelizeYCtrl, wx.GBPosition( 5, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_panelizeYLabel = wx.StaticText( m_fabBaseInfo.GetStaticBox(), wx.ID_ANY, _(u"Y:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panelizeYLabel.Wrap( -1 )

		m_fabBaseInfoSizer.Add( self.m_panelizeYLabel, wx.GBPosition( 5, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_RIGHT|wx.ALL, 5 )

		self.m_panelizeYUnit = wx.StaticText( m_fabBaseInfo.GetStaticBox(), wx.ID_ANY, _(u"pcs"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panelizeYUnit.Wrap( -1 )

		m_fabBaseInfoSizer.Add( self.m_panelizeYUnit, wx.GBPosition( 5, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_sizeLabel = wx.StaticText( m_fabBaseInfo.GetStaticBox(), wx.ID_ANY, _(u"Size (single):"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_sizeLabel.Wrap( -1 )

		m_fabBaseInfoSizer.Add( self.m_sizeLabel, wx.GBPosition( 6, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_sizeXLabel = wx.StaticText( m_fabBaseInfo.GetStaticBox(), wx.ID_ANY, _(u"X:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_sizeXLabel.Wrap( -1 )

		m_fabBaseInfoSizer.Add( self.m_sizeXLabel, wx.GBPosition( 7, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_RIGHT|wx.ALL, 5 )

		self.m_sizeXCtrl = wx.TextCtrl( m_fabBaseInfo.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 100,-1 ), wx.TE_READONLY )
		self.m_sizeXCtrl.SetMaxLength( 0 )
		m_fabBaseInfoSizer.Add( self.m_sizeXCtrl, wx.GBPosition( 7, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_sizeXUnit = wx.StaticText( m_fabBaseInfo.GetStaticBox(), wx.ID_ANY, _(u"mm"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_sizeXUnit.Wrap( -1 )

		m_fabBaseInfoSizer.Add( self.m_sizeXUnit, wx.GBPosition( 7, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_sizeYLabel1 = wx.StaticText( m_fabBaseInfo.GetStaticBox(), wx.ID_ANY, _(u"Y:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_sizeYLabel1.Wrap( -1 )

		m_fabBaseInfoSizer.Add( self.m_sizeYLabel1, wx.GBPosition( 8, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_RIGHT|wx.ALL, 5 )

		self.m_sizeYCtrl = wx.TextCtrl( m_fabBaseInfo.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 100,-1 ), wx.TE_READONLY )
		self.m_sizeYCtrl.SetMaxLength( 0 )
		m_fabBaseInfoSizer.Add( self.m_sizeYCtrl, wx.GBPosition( 8, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_sizeYUnit = wx.StaticText( m_fabBaseInfo.GetStaticBox(), wx.ID_ANY, _(u"mm"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_sizeYUnit.Wrap( -1 )

		m_fabBaseInfoSizer.Add( self.m_sizeYUnit, wx.GBPosition( 8, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_quantityLbel = wx.StaticText( m_fabBaseInfo.GetStaticBox(), wx.ID_ANY, _(u"Qty(single):"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_quantityLbel.Wrap( -1 )

		m_fabBaseInfoSizer.Add( self.m_quantityLbel, wx.GBPosition( 9, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_quantityCtrlChoices = [ _(u"5"), _(u"10"), _(u"15"), _(u"20"), _(u"25"), _(u"30"), _(u"40"), _(u"50"), _(u"75"), _(u"100"), _(u"125"), _(u"150"), _(u"200"), _(u"250"), _(u"300"), _(u"350"), _(u"400"), _(u"450"), _(u"500"), _(u"600"), _(u"700"), _(u"800"), _(u"900"), _(u"1000"), _(u"1500"), _(u"2000"), _(u"2500"), _(u"3000"), _(u"3500"), _(u"4000"), _(u"4500"), _(u"5000"), _(u"5500"), _(u"6000"), _(u"6500"), _(u"7000"), _(u"7500"), _(u"8000"), _(u"9000"), _(u"10000") ]
		self.m_quantityCtrl = wx.Choice( m_fabBaseInfo.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size( 100,-1 ), m_quantityCtrlChoices, 0 )
		self.m_quantityCtrl.SetSelection( 0 )
		m_fabBaseInfoSizer.Add( self.m_quantityCtrl, wx.GBPosition( 9, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_quantityUnit = wx.StaticText( m_fabBaseInfo.GetStaticBox(), wx.ID_ANY, _(u"Pcs"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_quantityUnit.Wrap( -1 )

		m_fabBaseInfoSizer.Add( self.m_quantityUnit, wx.GBPosition( 9, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_marginLabel = wx.StaticText( m_fabBaseInfo.GetStaticBox(), wx.ID_ANY, _(u"Break-away Rail:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_marginLabel.Wrap( -1 )

		m_fabBaseInfoSizer.Add( self.m_marginLabel, wx.GBPosition( 10, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_marginModeCtrlChoices = [ _(u"N/A"), _(u"Left & Right"), _(u"Top & Bottom"), _(u"All 4 sides") ]
		self.m_marginModeCtrl = wx.Choice( m_fabBaseInfo.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size( 100,-1 ), m_marginModeCtrlChoices, 0 )
		self.m_marginModeCtrl.SetSelection( 0 )
		m_fabBaseInfoSizer.Add( self.m_marginModeCtrl, wx.GBPosition( 10, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_marginValueCtrl = wx.TextCtrl( m_fabBaseInfo.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 100,-1 ), wx.TE_READONLY )
		self.m_marginValueCtrl.SetMaxLength( 0 )
		m_fabBaseInfoSizer.Add( self.m_marginValueCtrl, wx.GBPosition( 11, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_marginValueUnit = wx.StaticText( m_fabBaseInfo.GetStaticBox(), wx.ID_ANY, _(u"mm"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_marginValueUnit.Wrap( -1 )

		m_fabBaseInfoSizer.Add( self.m_marginValueUnit, wx.GBPosition( 11, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )


		m_fabBaseInfoSizer.AddGrowableCol( 1 )

		m_fabBaseInfo.Add( m_fabBaseInfoSizer, 1, wx.EXPAND, 5 )


		m_panelFabSizer.Add( m_fabBaseInfo, 0, wx.ALL|wx.EXPAND, 5 )

		m_fabProcessInfo = wx.StaticBoxSizer( wx.StaticBox( self.m_panelFab, wx.ID_ANY, _(u"Process info") ), wx.VERTICAL )

		m_fabProcessInfoSizer = wx.GridBagSizer( 0, 0 )
		m_fabProcessInfoSizer.SetFlexibleDirection( wx.BOTH )
		m_fabProcessInfoSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_boardThicknessLabel = wx.StaticText( m_fabProcessInfo.GetStaticBox(), wx.ID_ANY, _(u"PCB Thickness:"), wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.m_boardThicknessLabel.Wrap( -1 )

		m_fabProcessInfoSizer.Add( self.m_boardThicknessLabel, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_boardThicknessCtrlChoices = [ _(u"0.6"), _(u"0.8"), _(u"1.0"), _(u"1.2"), _(u"1.6"), _(u"2.0"), _(u"2.5"), _(u"3.0"), _(u"3.2") ]
		self.m_boardThicknessCtrl = wx.Choice( m_fabProcessInfo.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size( 100,-1 ), m_boardThicknessCtrlChoices, 0 )
		self.m_boardThicknessCtrl.SetSelection( 4 )
		m_fabProcessInfoSizer.Add( self.m_boardThicknessCtrl, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

		self.m_boardThicknessUnit = wx.StaticText( m_fabProcessInfo.GetStaticBox(), wx.ID_ANY, _(u"mm"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_boardThicknessUnit.Wrap( -1 )

		m_fabProcessInfoSizer.Add( self.m_boardThicknessUnit, wx.GBPosition( 0, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_outerCopperThicknessLabel = wx.StaticText( m_fabProcessInfo.GetStaticBox(), wx.ID_ANY, _(u"Finished Copper Weight:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_outerCopperThicknessLabel.Wrap( -1 )

		m_fabProcessInfoSizer.Add( self.m_outerCopperThicknessLabel, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_outerCopperThicknessCtrlChoices = [ _(u"1oz"), _(u"2oz") ]
		self.m_outerCopperThicknessCtrl = wx.Choice( m_fabProcessInfo.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size( 100,-1 ), m_outerCopperThicknessCtrlChoices, 0 )
		self.m_outerCopperThicknessCtrl.SetSelection( 0 )
		m_fabProcessInfoSizer.Add( self.m_outerCopperThicknessCtrl, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		self.m_innerCopperThicknessLabel = wx.StaticText( m_fabProcessInfo.GetStaticBox(), wx.ID_ANY, _(u"Inner Copper Weight:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_innerCopperThicknessLabel.Wrap( -1 )

		m_fabProcessInfoSizer.Add( self.m_innerCopperThicknessLabel, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_innerCopperThicknessCtrlChoices = [ _(u"0.5oz"), _(u"1oz"), _(u"2oz") ]
		self.m_innerCopperThicknessCtrl = wx.Choice( m_fabProcessInfo.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size( 100,-1 ), m_innerCopperThicknessCtrlChoices, 0 )
		self.m_innerCopperThicknessCtrl.SetSelection( 0 )
		m_fabProcessInfoSizer.Add( self.m_innerCopperThicknessCtrl, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		self.m_minTraceWidthClearanceLabel = wx.StaticText( m_fabProcessInfo.GetStaticBox(), wx.ID_ANY, _(u"Min Trace/Space Outer:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_minTraceWidthClearanceLabel.Wrap( -1 )

		m_fabProcessInfoSizer.Add( self.m_minTraceWidthClearanceLabel, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_minTraceWidthClearanceCtrlChoices = [ _(u"10/10mil"), _(u"8/8mil"), _(u"6/6mil"), _(u"5/5mil"), _(u"4/4mil"), _(u"3.5/3.5mil") ]
		self.m_minTraceWidthClearanceCtrl = wx.Choice( m_fabProcessInfo.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size( 100,-1 ), m_minTraceWidthClearanceCtrlChoices, 0 )
		self.m_minTraceWidthClearanceCtrl.SetSelection( 2 )
		m_fabProcessInfoSizer.Add( self.m_minTraceWidthClearanceCtrl, wx.GBPosition( 3, 1 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		self.m_minHoleSizeLabel = wx.StaticText( m_fabProcessInfo.GetStaticBox(), wx.ID_ANY, _(u"Min Drilled Hole:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_minHoleSizeLabel.Wrap( -1 )

		m_fabProcessInfoSizer.Add( self.m_minHoleSizeLabel, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_minHoleSizeCtrlChoices = [ _(u"0.3mm"), _(u"0.25mm"), _(u"0.2mm"), _(u"0.15mm") ]
		self.m_minHoleSizeCtrl = wx.Choice( m_fabProcessInfo.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size( 100,-1 ), m_minHoleSizeCtrlChoices, 0 )
		self.m_minHoleSizeCtrl.SetSelection( 0 )
		m_fabProcessInfoSizer.Add( self.m_minHoleSizeCtrl, wx.GBPosition( 4, 1 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		self.m_solderColorLabel = wx.StaticText( m_fabProcessInfo.GetStaticBox(), wx.ID_ANY, _(u"Solder Mask Color:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_solderColorLabel.Wrap( -1 )

		m_fabProcessInfoSizer.Add( self.m_solderColorLabel, wx.GBPosition( 5, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_solderColorCtrlChoices = [ _(u"Green"), _(u"Red"), _(u"Yellow"), _(u"Blue"), _(u"White"), _(u"Matte Black"), _(u"Black") ]
		self.m_solderColorCtrl = wx.Choice( m_fabProcessInfo.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size( 100,-1 ), m_solderColorCtrlChoices, 0 )
		self.m_solderColorCtrl.SetSelection( 0 )
		m_fabProcessInfoSizer.Add( self.m_solderColorCtrl, wx.GBPosition( 5, 1 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		self.m_silkscreenColorLabel = wx.StaticText( m_fabProcessInfo.GetStaticBox(), wx.ID_ANY, _(u"Silkscreen:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_silkscreenColorLabel.Wrap( -1 )

		m_fabProcessInfoSizer.Add( self.m_silkscreenColorLabel, wx.GBPosition( 6, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_silkscreenColorCtrlChoices = [ _(u"White") ]
		self.m_silkscreenColorCtrl = wx.Choice( m_fabProcessInfo.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size( 100,-1 ), m_silkscreenColorCtrlChoices, 0 )
		self.m_silkscreenColorCtrl.SetSelection( 0 )
		m_fabProcessInfoSizer.Add( self.m_silkscreenColorCtrl, wx.GBPosition( 6, 1 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		self.m_solderCoverLabel = wx.StaticText( m_fabProcessInfo.GetStaticBox(), wx.ID_ANY, _(u"Via Process:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_solderCoverLabel.Wrap( -1 )

		m_fabProcessInfoSizer.Add( self.m_solderCoverLabel, wx.GBPosition( 7, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_solderCoverCtrlChoices = [ _(u"Tenting Vias"), _(u"Vias not covered"), _(u"Solder Mask Plug (IV-B)"), _(u"Non-Conductive Fill") ]
		self.m_solderCoverCtrl = wx.Choice( m_fabProcessInfo.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size( 100,-1 ), m_solderCoverCtrlChoices, 0 )
		self.m_solderCoverCtrl.SetSelection( 0 )
		m_fabProcessInfoSizer.Add( self.m_solderCoverCtrl, wx.GBPosition( 7, 1 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		self.m_surfaceProcessLabel = wx.StaticText( m_fabProcessInfo.GetStaticBox(), wx.ID_ANY, _(u"Surface Finish:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_surfaceProcessLabel.Wrap( -1 )

		m_fabProcessInfoSizer.Add( self.m_surfaceProcessLabel, wx.GBPosition( 8, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_surfaceProcessCtrlChoices = [ _(u"HASL"), _(u"Lead free HASL"), _(u"ENIG"), _(u"OSP") ]
		self.m_surfaceProcessCtrl = wx.Choice( m_fabProcessInfo.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size( 100,-1 ), m_surfaceProcessCtrlChoices, 0 )
		self.m_surfaceProcessCtrl.SetSelection( 0 )
		m_fabProcessInfoSizer.Add( self.m_surfaceProcessCtrl, wx.GBPosition( 8, 1 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

		self.m_goldThicknessLabel = wx.StaticText( m_fabProcessInfo.GetStaticBox(), wx.ID_ANY, _(u"Immersion Gold Thickness:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_goldThicknessLabel.Wrap( -1 )

		m_fabProcessInfoSizer.Add( self.m_goldThicknessLabel, wx.GBPosition( 9, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_goldThicknessCtrlChoices = [ _(u"1µm"), _(u"2µm"), _(u"3µm") ]
		self.m_goldThicknessCtrl = wx.Choice( m_fabProcessInfo.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size( 100,-1 ), m_goldThicknessCtrlChoices, 0 )
		self.m_goldThicknessCtrl.SetSelection( 0 )
		m_fabProcessInfoSizer.Add( self.m_goldThicknessCtrl, wx.GBPosition( 9, 1 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )


		m_fabProcessInfoSizer.AddGrowableCol( 1 )

		m_fabProcessInfo.Add( m_fabProcessInfoSizer, 1, wx.EXPAND, 5 )


		m_panelFabSizer.Add( m_fabProcessInfo, 0, wx.ALL|wx.EXPAND, 5 )

		m_fabSpecialProcess = wx.StaticBoxSizer( wx.StaticBox( self.m_panelFab, wx.ID_ANY, _(u"Special Process") ), wx.VERTICAL )

		m_fabSpecialProcessSizer = wx.GridBagSizer( 0, 0 )
		m_fabSpecialProcessSizer.SetFlexibleDirection( wx.BOTH )
		m_fabSpecialProcessSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_impedanceLabel = wx.StaticText( m_fabSpecialProcess.GetStaticBox(), wx.ID_ANY, _(u"Impedance:"), wx.DefaultPosition, wx.Size( 100,-1 ), 0 )
		self.m_impedanceLabel.Wrap( -1 )

		m_fabSpecialProcessSizer.Add( self.m_impedanceLabel, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_impedanceCtrlChoices = [ _(u"No"), _(u"Yes") ]
		self.m_impedanceCtrl = wx.Choice( m_fabSpecialProcess.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size( 100,-1 ), m_impedanceCtrlChoices, 0 )
		self.m_impedanceCtrl.SetSelection( 0 )
		m_fabSpecialProcessSizer.Add( self.m_impedanceCtrl, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 3 ), wx.ALL|wx.EXPAND, 5 )

		self.m_goldFingerLabel = wx.StaticText( m_fabSpecialProcess.GetStaticBox(), wx.ID_ANY, _(u"Beveling of G/F:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_goldFingerLabel.Wrap( -1 )

		m_fabSpecialProcessSizer.Add( self.m_goldFingerLabel, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_goldFingerCtrlChoices = [ _(u"No"), _(u"Yes") ]
		self.m_goldFingerCtrl = wx.Choice( m_fabSpecialProcess.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size( 100,-1 ), m_goldFingerCtrlChoices, 0 )
		self.m_goldFingerCtrl.SetSelection( 0 )
		m_fabSpecialProcessSizer.Add( self.m_goldFingerCtrl, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 3 ), wx.ALL|wx.EXPAND, 5 )

		self.m_halfHoleLabel = wx.StaticText( m_fabSpecialProcess.GetStaticBox(), wx.ID_ANY, _(u"Plated Half Holes:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_halfHoleLabel.Wrap( -1 )

		m_fabSpecialProcessSizer.Add( self.m_halfHoleLabel, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_halfHoleCtrlChoices = [ _(u"No"), _(u"Yes") ]
		self.m_halfHoleCtrl = wx.Choice( m_fabSpecialProcess.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size( 100,-1 ), m_halfHoleCtrlChoices, 0 )
		self.m_halfHoleCtrl.SetSelection( 0 )
		m_fabSpecialProcessSizer.Add( self.m_halfHoleCtrl, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 3 ), wx.ALL|wx.EXPAND, 5 )

		self.m_padHoleLabel = wx.StaticText( m_fabSpecialProcess.GetStaticBox(), wx.ID_ANY, _(u"Pad Hole:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_padHoleLabel.Wrap( -1 )

		m_fabSpecialProcessSizer.Add( self.m_padHoleLabel, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_padHoleCtrlChoices = [ _(u"No"), _(u"Yes") ]
		self.m_padHoleCtrl = wx.Choice( m_fabSpecialProcess.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size( 100,-1 ), m_padHoleCtrlChoices, 0 )
		self.m_padHoleCtrl.SetSelection( 0 )
		m_fabSpecialProcessSizer.Add( self.m_padHoleCtrl, wx.GBPosition( 3, 1 ), wx.GBSpan( 1, 3 ), wx.ALL|wx.EXPAND, 5 )

		self.m_blindViaLabel = wx.StaticText( m_fabSpecialProcess.GetStaticBox(), wx.ID_ANY, _(u"HDI(Buried/blind vias):"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_blindViaLabel.Wrap( -1 )

		m_fabSpecialProcessSizer.Add( self.m_blindViaLabel, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_blindViaCtrlChoices = [ _(u"No"), _(u"Yes") ]
		self.m_blindViaCtrl = wx.Choice( m_fabSpecialProcess.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_blindViaCtrlChoices, 0 )
		self.m_blindViaCtrl.SetSelection( 0 )
		m_fabSpecialProcessSizer.Add( self.m_blindViaCtrl, wx.GBPosition( 4, 1 ), wx.GBSpan( 1, 3 ), wx.ALL|wx.EXPAND, 5 )

		self.m_hdiStructureLabel = wx.StaticText( m_fabSpecialProcess.GetStaticBox(), wx.ID_ANY, _(u"HDI Structure:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_hdiStructureLabel.Wrap( -1 )

		m_fabSpecialProcessSizer.Add( self.m_hdiStructureLabel, wx.GBPosition( 5, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_hdiStructureCtrlChoices = [ _(u"Rank 1"), _(u"Rank 2"), _(u"Rank 3") ]
		self.m_hdiStructureCtrl = wx.Choice( m_fabSpecialProcess.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size( 100,-1 ), m_hdiStructureCtrlChoices, 0 )
		self.m_hdiStructureCtrl.SetSelection( 0 )
		m_fabSpecialProcessSizer.Add( self.m_hdiStructureCtrl, wx.GBPosition( 5, 1 ), wx.GBSpan( 1, 3 ), wx.ALL|wx.EXPAND, 5 )

		self.m_stackupLabel = wx.StaticText( m_fabSpecialProcess.GetStaticBox(), wx.ID_ANY, _(u"Stack up:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_stackupLabel.Wrap( -1 )

		m_fabSpecialProcessSizer.Add( self.m_stackupLabel, wx.GBPosition( 6, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_stackupCtrlChoices = [ _(u"No Requirement"), _(u"Customer Specified Stack up") ]
		self.m_stackupCtrl = wx.Choice( m_fabSpecialProcess.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size( 100,-1 ), m_stackupCtrlChoices, 0 )
		self.m_stackupCtrl.SetSelection( 0 )
		m_fabSpecialProcessSizer.Add( self.m_stackupCtrl, wx.GBPosition( 6, 1 ), wx.GBSpan( 1, 3 ), wx.ALL|wx.EXPAND, 5 )


		m_fabSpecialProcessSizer.AddGrowableCol( 1 )

		m_fabSpecialProcess.Add( m_fabSpecialProcessSizer, 1, wx.EXPAND, 5 )


		m_panelFabSizer.Add( m_fabSpecialProcess, 0, wx.ALL|wx.EXPAND, 5 )

		m_fabServiceInfo = wx.StaticBoxSizer( wx.StaticBox( self.m_panelFab, wx.ID_ANY, _(u"Personalized Service") ), wx.VERTICAL )

		m_fabServiceInfoSizer = wx.GridBagSizer( 0, 0 )
		m_fabServiceInfoSizer.SetFlexibleDirection( wx.BOTH )
		m_fabServiceInfoSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_testMethodLabel = wx.StaticText( m_fabServiceInfo.GetStaticBox(), wx.ID_ANY, _(u"Electrical Test:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_testMethodLabel.Wrap( -1 )

		m_fabServiceInfoSizer.Add( self.m_testMethodLabel, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_testMethodCtrlChoices = [ _(u"Sample Test Free"), _(u"AOI+Flying Test"), _(u"AOI+Fixture") ]
		self.m_testMethodCtrl = wx.Choice( m_fabServiceInfo.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size( 100,-1 ), m_testMethodCtrlChoices, 0 )
		self.m_testMethodCtrl.SetSelection( 0 )
		m_fabServiceInfoSizer.Add( self.m_testMethodCtrl, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 3 ), wx.ALL|wx.EXPAND, 5 )

		self.m_approveWorkingGerberLabel = wx.StaticText( m_fabServiceInfo.GetStaticBox(), wx.ID_ANY, _(u"Approve Working Gerber:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_approveWorkingGerberLabel.Wrap( -1 )

		m_fabServiceInfoSizer.Add( self.m_approveWorkingGerberLabel, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_approveWorkingGerberCtrlChoices = [ _(u"No"), _(u"Yes") ]
		self.m_approveWorkingGerberCtrl = wx.Choice( m_fabServiceInfo.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size( 100,-1 ), m_approveWorkingGerberCtrlChoices, 0 )
		self.m_approveWorkingGerberCtrl.SetSelection( 0 )
		m_fabServiceInfoSizer.Add( self.m_approveWorkingGerberCtrl, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 3 ), wx.ALL|wx.EXPAND, 5 )

		self.m_deliveryReportLabel = wx.StaticText( m_fabServiceInfo.GetStaticBox(), wx.ID_ANY, _(u"Delivery Report:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_deliveryReportLabel.Wrap( -1 )

		m_fabServiceInfoSizer.Add( self.m_deliveryReportLabel, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_deliveryReportCtrlChoices = [ _(u"No"), _(u"Yes") ]
		self.m_deliveryReportCtrl = wx.Choice( m_fabServiceInfo.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size( 100,-1 ), m_deliveryReportCtrlChoices, 0 )
		self.m_deliveryReportCtrl.SetSelection( 0 )
		m_fabServiceInfoSizer.Add( self.m_deliveryReportCtrl, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 3 ), wx.ALL|wx.EXPAND, 5 )

		self.m_analysisReportLabel = wx.StaticText( m_fabServiceInfo.GetStaticBox(), wx.ID_ANY, _(u"Microsection Analysis Report:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_analysisReportLabel.Wrap( -1 )

		m_fabServiceInfoSizer.Add( self.m_analysisReportLabel, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_analysisReportCtrlChoices = [ _(u"No"), _(u"Yes") ]
		self.m_analysisReportCtrl = wx.Choice( m_fabServiceInfo.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size( 100,-1 ), m_analysisReportCtrlChoices, 0 )
		self.m_analysisReportCtrl.SetSelection( 0 )
		m_fabServiceInfoSizer.Add( self.m_analysisReportCtrl, wx.GBPosition( 3, 1 ), wx.GBSpan( 1, 3 ), wx.ALL|wx.EXPAND, 5 )

		self.m_reportFormatLabel = wx.StaticText( m_fabServiceInfo.GetStaticBox(), wx.ID_ANY, _(u"Report Format:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_reportFormatLabel.Wrap( -1 )

		m_fabServiceInfoSizer.Add( self.m_reportFormatLabel, wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_reportFormatCtrlChoices = [ _(u"Paper"), _(u"Electronic") ]
		self.m_reportFormatCtrl = wx.Choice( m_fabServiceInfo.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size( 100,-1 ), m_reportFormatCtrlChoices, 0 )
		self.m_reportFormatCtrl.SetSelection( 1 )
		m_fabServiceInfoSizer.Add( self.m_reportFormatCtrl, wx.GBPosition( 4, 1 ), wx.GBSpan( 1, 3 ), wx.ALL|wx.EXPAND, 5 )

		self.m_ulMarkLabel = wx.StaticText( m_fabServiceInfo.GetStaticBox(), wx.ID_ANY, _(u"UL Mark:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_ulMarkLabel.Wrap( -1 )

		m_fabServiceInfoSizer.Add( self.m_ulMarkLabel, wx.GBPosition( 5, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_ulMarkCtrlChoices = [ _(u"No"), _(u"UL+Week/Year"), _(u"UL+Year/Week") ]
		self.m_ulMarkCtrl = wx.Choice( m_fabServiceInfo.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size( 100,-1 ), m_ulMarkCtrlChoices, 0 )
		self.m_ulMarkCtrl.SetSelection( 0 )
		m_fabServiceInfoSizer.Add( self.m_ulMarkCtrl, wx.GBPosition( 5, 1 ), wx.GBSpan( 1, 3 ), wx.ALL|wx.EXPAND, 5 )

		self.m_filmLabel = wx.StaticText( m_fabServiceInfo.GetStaticBox(), wx.ID_ANY, _(u"Film:"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_filmLabel.Wrap( -1 )

		m_fabServiceInfoSizer.Add( self.m_filmLabel, wx.GBPosition( 6, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		m_filmCtrlChoices = [ _(u"No"), _(u"Yes") ]
		self.m_filmCtrl = wx.Choice( m_fabServiceInfo.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.Size( 100,-1 ), m_filmCtrlChoices, 0 )
		self.m_filmCtrl.SetSelection( 0 )
		m_fabServiceInfoSizer.Add( self.m_filmCtrl, wx.GBPosition( 6, 1 ), wx.GBSpan( 1, 3 ), wx.ALL|wx.EXPAND, 5 )

		self.m_specialRequestsLabel = wx.StaticText( m_fabServiceInfo.GetStaticBox(), wx.ID_ANY, _(u"Special Requests:"), wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.m_specialRequestsLabel.Wrap( -1 )

		m_fabServiceInfoSizer.Add( self.m_specialRequestsLabel, wx.GBPosition( 7, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

		self.m_specialRequestsCtrl = wx.TextCtrl( m_fabServiceInfo.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 100,-1 ), 0 )
		m_fabServiceInfoSizer.Add( self.m_specialRequestsCtrl, wx.GBPosition( 7, 1 ), wx.GBSpan( 5, 3 ), wx.ALL|wx.EXPAND, 5 )


		m_fabServiceInfoSizer.AddGrowableCol( 1 )

		m_fabServiceInfo.Add( m_fabServiceInfoSizer, 1, wx.EXPAND, 5 )


		m_panelFabSizer.Add( m_fabServiceInfo, 0, wx.ALL|wx.EXPAND, 5 )


		self.m_panelFab.SetSizer( m_panelFabSizer )
		self.m_panelFab.Layout()
		m_panelFabSizer.Fit( self.m_panelFab )
		self.m_notebook.AddPage( self.m_panelFab, _(u"PCB Fabrication"), False )

		m_topLeftSizer.Add( self.m_notebook, 1, wx.ALIGN_CENTER|wx.EXPAND|wx.TOP, 12 )


		m_topSizer.Add( m_topLeftSizer, 6, wx.ALL|wx.EXPAND, 5 )

		m_topRightSizer = wx.BoxSizer( wx.VERTICAL )

		m_totalSummarySizer = wx.GridBagSizer( 0, 0 )
		m_totalSummarySizer.SetFlexibleDirection( wx.BOTH )
		m_totalSummarySizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_huaqiuLogo = wx.StaticBitmap( self, wx.ID_ANY, wx.Bitmap( self.GetImagePath( u"Huaqiu.png" ), wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, 0 )
		m_totalSummarySizer.Add( self.m_huaqiuLogo, wx.GBPosition( 0, 0 ), wx.GBSpan( 3, 1 ), wx.ALL|wx.EXPAND|wx.RIGHT|wx.TOP, 5 )

		self.m_amountLabel = wx.StaticText( self, wx.ID_ANY, _(u"PCB Qty："), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_amountLabel.Wrap( -1 )

		m_totalSummarySizer.Add( self.m_amountLabel, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.LEFT|wx.TOP, 5 )

		self.m_amountCtrl = wx.StaticText( self, wx.ID_ANY, _(u"-"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_amountCtrl.Wrap( -1 )

		m_totalSummarySizer.Add( self.m_amountCtrl, wx.GBPosition( 0, 2 ), wx.GBSpan( 1, 1 ), wx.TOP, 5 )

		self.m_amountUnit = wx.StaticText( self, wx.ID_ANY, _(u"pcs"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_amountUnit.Wrap( -1 )

		m_totalSummarySizer.Add( self.m_amountUnit, wx.GBPosition( 0, 3 ), wx.GBSpan( 1, 1 ), wx.LEFT|wx.TOP, 5 )

		self.m_dueDateLabel = wx.StaticText( self, wx.ID_ANY, _(u"Time："), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_dueDateLabel.Wrap( -1 )

		m_totalSummarySizer.Add( self.m_dueDateLabel, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.LEFT, 5 )

		self.m_dueDateCtrl = wx.StaticText( self, wx.ID_ANY, _(u"-"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_dueDateCtrl.Wrap( -1 )

		m_totalSummarySizer.Add( self.m_dueDateCtrl, wx.GBPosition( 1, 2 ), wx.GBSpan( 1, 1 ), 0, 5 )

		self.m_dueDateUnit = wx.StaticText( self, wx.ID_ANY, _(u"Days"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_dueDateUnit.Wrap( -1 )

		m_totalSummarySizer.Add( self.m_dueDateUnit, wx.GBPosition( 1, 3 ), wx.GBSpan( 1, 1 ), wx.LEFT, 5 )

		self.m_priceLabel = wx.StaticText( self, wx.ID_ANY, _(u"Cost："), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_priceLabel.Wrap( -1 )

		m_totalSummarySizer.Add( self.m_priceLabel, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.LEFT|wx.TOP, 5 )

		self.m_priceCtrl = wx.StaticText( self, wx.ID_ANY, _(u"-"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_priceCtrl.Wrap( -1 )

		m_totalSummarySizer.Add( self.m_priceCtrl, wx.GBPosition( 2, 2 ), wx.GBSpan( 1, 1 ), wx.TOP, 5 )

		self.m_priceUnit = wx.StaticText( self, wx.ID_ANY, _(u"$"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_priceUnit.Wrap( -1 )

		m_totalSummarySizer.Add( self.m_priceUnit, wx.GBPosition( 2, 3 ), wx.GBSpan( 1, 1 ), wx.LEFT|wx.TOP, 5 )

		self.m_updatePriceButton = wx.Button( self, wx.ID_ANY, _(u"Update Price"), wx.DefaultPosition, wx.DefaultSize, 0 )
		m_totalSummarySizer.Add( self.m_updatePriceButton, wx.GBPosition( 2, 4 ), wx.GBSpan( 1, 1 ), wx.BOTTOM|wx.EXPAND|wx.RIGHT, 5 )

		self.m_placeOrderButton = wx.Button( self, wx.ID_ANY, _(u"Place Order"), wx.DefaultPosition, wx.DefaultSize, 0 )
		m_totalSummarySizer.Add( self.m_placeOrderButton, wx.GBPosition( 0, 4 ), wx.GBSpan( 1, 1 ), wx.EXPAND|wx.RIGHT|wx.TOP, 5 )


		m_totalSummarySizer.AddGrowableCol( 2 )
		m_totalSummarySizer.AddGrowableCol( 3 )

		m_topRightSizer.Add( m_totalSummarySizer, 0, wx.EXPAND, 5 )

		self.m_priceDetailsViewListCtrl = wx.dataview.DataViewListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_priceDescriptionColumn = self.m_priceDetailsViewListCtrl.AppendTextColumn( _(u"Item"), wx.dataview.DATAVIEW_CELL_INERT, 200, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_RESIZABLE )
		self.m_priceColumn = self.m_priceDetailsViewListCtrl.AppendTextColumn( _(u"Price"), wx.dataview.DATAVIEW_CELL_INERT, -1, wx.ALIGN_LEFT, wx.dataview.DATAVIEW_COL_RESIZABLE )
		m_topRightSizer.Add( self.m_priceDetailsViewListCtrl, 1, wx.ALL|wx.EXPAND, 5 )

		self.m_drcPanel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.BORDER_SIMPLE|wx.TAB_TRAVERSAL )
		m_drcPanelSizer = wx.BoxSizer( wx.VERTICAL )


		self.m_drcPanel.SetSizer( m_drcPanelSizer )
		self.m_drcPanel.Layout()
		m_drcPanelSizer.Fit( self.m_drcPanel )
		m_topRightSizer.Add( self.m_drcPanel, 1, wx.ALL|wx.EXPAND, 5 )


		m_topSizer.Add( m_topRightSizer, 5, wx.ALL|wx.EXPAND, 5 )


		m_mainSizer.Add( m_topSizer, 1, wx.EXPAND, 8 )


		self.SetSizer( m_mainSizer )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_template.Bind( wx.EVT_CHOICE, self.OnTemplateChanged )
		self.m_pcbPackaingCtrl.Bind( wx.EVT_CHOICE, self.OnPcbPackagingChanged )
		self.m_panelizeXCtrl.Bind( wx.EVT_TEXT, self.OnPanelizeXChanged )
		self.m_panelizeYCtrl.Bind( wx.EVT_TEXT, self.OnPanelizeYChanged )
		self.m_quantityCtrl.Bind( wx.EVT_CHOICE, self.OnPcbQuantityChanged )
		self.m_marginModeCtrl.Bind( wx.EVT_CHOICE, self.OnMarginModeChanged )
		self.m_surfaceProcessCtrl.Bind( wx.EVT_CHOICE, self.OnSurfaceProcessChanged )
		self.m_blindViaCtrl.Bind( wx.EVT_CHOICE, self.OnHDIChanged )
		self.m_deliveryReportCtrl.Bind( wx.EVT_CHOICE, self.OnReportChanged )
		self.m_analysisReportCtrl.Bind( wx.EVT_CHOICE, self.OnReportChanged )
		self.m_updatePriceButton.Bind( wx.EVT_BUTTON, self.OnUpdatePrice )
		self.m_placeOrderButton.Bind( wx.EVT_BUTTON, self.OnPlaceOrder )
		self.m_solderColorCtrl.Bind( wx.EVT_CHOICE, self.OnMaskColorChange )
		#self.m_layerCountCtrl.Bind( wx.EVT_CHOICE, self.OnTGChangebyLayer )
		self.m_layerCountCtrl.Bind( wx.EVT_CHOICE, self.OnThicknessChangebyLayer )


	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def OnTemplateChanged( self, event ):
		event.Skip()

	def OnPcbPackagingChanged( self, event ):
		event.Skip()

	def OnPanelizeXChanged( self, event ):
		event.Skip()

	def OnPanelizeYChanged( self, event ):
		event.Skip()

	def OnPcbQuantityChanged( self, event ):
		event.Skip()

	def OnMarginModeChanged( self, event ):
		event.Skip()

	def OnSurfaceProcessChanged( self, event ):
		event.Skip()

	def OnHDIChanged( self, event ):
		event.Skip()

	def OnReportChanged( self, event ):
		event.Skip()


	def OnUpdatePrice( self, event ):
		event.Skip()

	def OnPlaceOrder( self, event ):
		event.Skip()

	def OnMaskColorChange(self, event):
		event.Skip()

	def OnThicknessChangebyLayer(self, event):
		event.Skip()

	# Virtual image path resolution method. Override this in your derived class.
	def GetImagePath( self, bitmap_path ):
		return bitmap_path


