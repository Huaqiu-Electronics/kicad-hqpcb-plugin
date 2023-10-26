import os
import wx
import wx.lib.masked as masked
import urllib.request
import urllib.parse
import json
import re
from .urlencodeform import UrlEncodeForm
from collections import defaultdict
import locale
from datetime import datetime
import requests
import webbrowser

import pcbnew
from . import dialog_amf_base
from .fabrication import Fabrication
import gettext
_ = gettext.gettext

from. import validators

# Implementing AmfDialogBase
class AmfDialog( dialog_amf_base.AmfDialogBase ):
    def __init__( self, parent ):
        dialog_amf_base.AmfDialogBase.__init__( self, parent )
        
        self.board = pcbnew.GetBoard()

        boardWidth = pcbnew.ToMM(self.board.GetBoardEdgesBoundingBox().GetWidth())
        boardHeight = pcbnew.ToMM(self.board.GetBoardEdgesBoundingBox().GetHeight())
        designSettings = self.board.GetDesignSettings()
        boardThickness = designSettings.GetBoardThickness()
        minTraceWidth = designSettings.m_TrackMinWidth
        minTraceClearance = designSettings.m_MinClearance
        minHoleSize = designSettings.m_MinThroughDrill
        layerCount = self.board.GetCopperLayerCount()
        self.load_config_file()
        self.m_layerCountCtrl.SetSelection(self.m_layerCountCtrl.FindString(str(layerCount)))
        self.OnThicknessChangebyLayer(None)
        self.m_layerCountCtrl.Enabled = False
        #self.m_placeOrderButton.Enabled = False
        self.m_sizeXCtrl.SetValue(str(boardWidth))
        self.m_sizeXCtrl.SetEditable(False)
        self.m_sizeYCtrl.SetValue(str(boardHeight))
        self.m_sizeYCtrl.SetEditable(False)
        # self.m_asmSizeXCtrl.SetValue(str(boardWidth))
        # self.m_asmSizeXCtrl.SetEditable(False)
        # self.m_asmSizeYCtrl.SetValue(str(boardHeight))
        # self.m_asmSizeYCtrl.SetEditable(False)
        self.SetBoardThickness(pcbnew.ToMM(boardThickness))
        self.SetMinTrace(pcbnew.ToMils(minTraceWidth), pcbnew.ToMils(minTraceClearance))
        self.SetMinHole(pcbnew.ToMM(minHoleSize))
        self.m_pcbPackaingCtrl.SetSelection(0)
        self.OnPcbPackagingChanged(None)
        self.m_marginModeCtrl.SetSelection(0)
        self.OnMarginModeChanged(None)
        self.m_surfaceProcessCtrl.SetSelection(0)
        self.OnSurfaceProcessChanged(None)
        self.numericValidator = validators.NumericTextCtrlValidator()
        self.m_panelizeXCtrl.SetValidator(self.numericValidator)
        self.m_panelizeYCtrl.SetValidator(self.numericValidator)
        self.floatValidator = validators.FloatTextCtrlValidator()
        self.m_marginValueCtrl.SetValidator(self.floatValidator) 
        if layerCount == 2:
            self.m_innerCopperThicknessLabel.Enabled = False
            self.m_innerCopperThicknessCtrl.Enabled = False
            self.m_blindViaLabel.Enabled = False
            self.m_blindViaCtrl.Enabled = False 
        else:
            self.m_innerCopperThicknessLabel.Enabled = True
            self.m_innerCopperThicknessCtrl.Enabled = True
            self.m_blindViaLabel.Enabled = True
            self.m_blindViaCtrl.Enabled = True 
        self.m_template.SetSelection(0)
        self.OnTemplateChanged(None)    
        self.OnPcbQuantityChanged(None)
        self.OnHDIChanged(None)
        #self.OnMaskColorChange(None)
        self.fabrication = None
        # self.SetSMTInfo()
        # self.SetDIPInfo()              
        
    # Handlers for AmfDialogBase events.
    def OnTemplateChanged( self, event ):
        if self.m_template.GetSelection() == 0 and self.m_notebook.PageCount > 1:
            self.m_notebook.RemovePage(1)
        elif self.m_template.GetSelection() == 1 and self.m_notebook.PageCount == 1:
            self.m_notebook.AddPage( self.m_panelAsm, _(u"PCB Assembly"), True )
            
    def OnPcbPackagingChanged(self, event):
        if self.m_pcbPackaingCtrl.GetSelection() == 0:
            self.m_sizeLabel.SetLabel('Size (single)')
            self.m_quantityLbel.SetLabel('Qty(single)')
            self.m_quantityUnit.SetLabel('Pcs')
            self.m_panelizeRuleLbel.Enabled = False
            self.m_panelizeXLabel.Enabled = False
            self.m_panelizeXCtrl.Enabled = False
            self.m_panelizeXUnit.Enabled = False
            self.m_panelizeYLabel.Enabled = False
            self.m_panelizeYCtrl.Enabled = False
            self.m_panelizeYUnit.Enabled = False
            self.m_marginLabel.Enabled = True
            self.m_marginModeCtrl.Enabled = True
            self.OnMarginModeChanged(None)
        else:
            self.m_sizeLabel.SetLabel('Size (set)')
            self.m_quantityLbel.SetLabel('Qty(Set)')
            self.m_quantityUnit.SetLabel('Set')
            self.m_panelizeRuleLbel.Enabled = True
            self.m_panelizeXLabel.Enabled = True
            self.m_panelizeXCtrl.Enabled = True
            self.m_panelizeXCtrl.SetEditable(True)
            self.m_panelizeXUnit.Enabled = True
            self.m_panelizeYLabel.Enabled = True
            self.m_panelizeYCtrl.Enabled = True
            self.m_panelizeYCtrl.SetEditable(True)
            self.m_panelizeYUnit.Enabled = True
            self.m_marginLabel.Enabled = True
            self.m_marginModeCtrl.Enabled = True
            self.OnMarginModeChanged(None)
        
    def OnMarginModeChanged( self, event ):
        if self.m_marginModeCtrl.GetSelection() == 0:
            self.m_marginValueCtrl.Enabled = False
            self.m_marginValueUnit.Enabled = False
        else:
            self.m_marginValueCtrl.Enabled = True
            self.m_marginValueCtrl.SetEditable(True)
            self.m_marginValueUnit.Enabled = True
            
    def OnSurfaceProcessChanged( self, event ):
        if self.m_surfaceProcessCtrl.GetSelection() == 2:
            self.m_goldThicknessLabel.Enabled = True
            self.m_goldThicknessCtrl.Enabled = True
        else:
            self.m_goldThicknessLabel.Enabled = False
            self.m_goldThicknessCtrl.Enabled = False

    def OnPanelizeXChanged( self, event ):
        if not self.m_panelizeXCtrl.Validate():
            wx.MessageBox("Panel Type X value isn't valid. Please input valid value.", "Error", wx.OK | wx.ICON_ERROR)
            return        
        # self.m_asmQuantityCtrl.SetValue(str(self.GetPcbQuantity()))
    
    def OnPanelizeYChanged( self, event ):
        if not self.m_panelizeYCtrl.Validate():
            wx.MessageBox("Panel Type Y value isn't valid. Please input valid value.", "Error", wx.OK | wx.ICON_ERROR)
            return
        # self.m_asmQuantityCtrl.SetValue(str(self.GetPcbQuantity()))

    def OnPcbQuantityChanged( self, event ):
        # self.m_asmQuantityCtrl.SetValue(str(self.GetPcbQuantity()))
        return

    def OnHDIChanged( self, event ):
        if self.m_blindViaCtrl.GetSelection() == 1:
            self.m_hdiStructureLabel.Enabled = True
            self.m_hdiStructureCtrl.Enabled = True
        else:
            self.m_hdiStructureLabel.Enabled = False
            self.m_hdiStructureCtrl.Enabled = False

    def OnReportChanged( self, event ):
        if self.m_deliveryReportCtrl.GetSelection() == 0 and self.m_analysisReportCtrl.GetSelection() == 0:
            self.m_reportFormatLabel.Enabled = False
            self.m_reportFormatCtrl.Enabled = False
        else:
            self.m_reportFormatLabel.Enabled = True
            self.m_reportFormatCtrl.Enabled = True

    def OnMaskColorChange(self, event):
        self.m_silkscreenColorCtrl.Clear()
        mask_color = self.m_solderColorCtrl.GetString(self.m_solderColorCtrl.GetSelection())
        val_list = self.config_json["rule"]["silkscreen"][mask_color]
        self.m_silkscreenColorCtrl.Append(val_list)
        self.m_silkscreenColorCtrl.SetSelection( 0 )

    def OnThicknessChangebyLayer(self, event):
        layer = self.m_layerCountCtrl.GetString(self.m_layerCountCtrl.GetSelection())
        self.m_boardThicknessCtrl.Clear()
        val_list = self.config_json["rule"]["thickness"][layer]
        self.m_boardThicknessCtrl.Append(val_list)
        

    def load_config_file(self):
        """Load config from config.json"""
        if not os.path.isfile(os.path.join(os.path.dirname(__file__), "config.json")):
            wx.MessageBox("Load config json file failed.Please reinstall plugin.", "Error", wx.OK | wx.ICON_ERROR)
            return        
        with open(os.path.join(os.path.dirname(__file__), "config.json")) as j:
            self.config_json = json.load(j)

    def init_fabrication(self):
        """Initialize the fabrication"""
        if not self.fabrication:
            self.fabrication = Fabrication(self)

    # def OnDoDIPChanged( self, event ):
    #     if self.m_doDIPCtrl.GetSelection() == 0:
    #         self.m_dipComponentKindsCtrl.SetEditable(False)
    #         self.m_dipPadCountCtrl.SetEditable(False)
    #     else:
    #         self.m_dipComponentKindsCtrl.SetEditable(True)
    #         self.m_dipPadCountCtrl.SetEditable(True)

    def GetInfoFromSetting(self):
        if self.m_pcbPackaingCtrl.GetSelection() == 1 or self.m_pcbPackaingCtrl.GetSelection() == 2:
            if not self.m_panelizeXCtrl.Validate():
                wx.MessageBox("Panel Type X value isn't valid. Please input valid value.", "Error", wx.OK | wx.ICON_ERROR)
                return
            if not self.m_panelizeYCtrl.Validate():
                wx.MessageBox("Panel Type Y value isn't valid. Please input valid value.", "Error", wx.OK | wx.ICON_ERROR)
                return
        if self.m_marginValueCtrl.Enabled:
            if not self.m_marginValueCtrl.Validate():
                wx.MessageBox("Break-away Rail value isn't valid. Please input valid value.", "Error", wx.OK | wx.ICON_ERROR)
                return
        
        form = UrlEncodeForm()
        form.add_field('service', 'pcb')
        form.add_field('plate_type', 'Fr-4')  #self.m_baseMaterialCtrl.GetString(self.m_baseMaterialCtrl.GetSelection()))
        layercount = int(self.m_layerCountCtrl.GetString(self.m_layerCountCtrl.GetSelection()))
        form.add_field('blayer', str(layercount))
        form.add_field('board_tg', 'TG130') #TODO
        if self.m_pcbPackaingCtrl.GetSelection() == 0:
            form.add_field('units', '1')
        elif self.m_pcbPackaingCtrl.GetSelection() == 1:
            form.add_field('units', '3')
        else:
            form.add_field('units', '2')
        form.add_field('blength', str(round(self.GetPcbLength() / 10, 2)))
        form.add_field('bwidth', str(round(self.GetPcbWidth() / 10, 2)))
        if self.m_pcbPackaingCtrl.GetSelection() == 1 or self.m_pcbPackaingCtrl.GetSelection() == 2:
            form.add_field('layoutx', self.m_panelizeXCtrl.GetValue())
            form.add_field('layouty', self.m_panelizeYCtrl.GetValue())
        form.add_field('bcount', self.m_quantityCtrl.GetString(self.m_quantityCtrl.GetSelection()))
        form.add_field('sidedirection', self.GetMarginMode())
        if self.m_marginModeCtrl.GetSelection() != 0:
            form.add_field('sidewidth', self.m_marginValueCtrl.GetValue())
        form.add_field('bheight', self.m_boardThicknessCtrl.GetString(self.m_boardThicknessCtrl.GetSelection()))
        form.add_field('copper', str(self.GetOuterCopperThickness()))
        if layercount > 2:
            form.add_field('insidecopper', str(self.GetInnerCopperThickness()))
            if self.m_stackupCtrl.GetSelection() == 0:
                form.add_field('pressing', '')
            else:
                form.add_field('pressing', 'Customer Specified Stack up')
        else:
            form.add_field('insidecopper', '0')
            form.add_field('pressing', '')
        form.add_field('lineweight', str(self.GetMinTraceWidthAndClearance()))
        form.add_field('vias', str(self.GetMinHoleSize()))
        form.add_field('color', self.m_solderColorCtrl.GetString(self.m_solderColorCtrl.GetSelection()))
        form.add_field('charcolor', self.m_silkscreenColorCtrl.GetString(self.m_silkscreenColorCtrl.GetSelection()))
        form.add_field('cover', self.m_solderCoverCtrl.GetString(self.m_solderCoverCtrl.GetSelection()))
        form.add_field('spray', self.m_surfaceProcessCtrl.GetString(self.m_surfaceProcessCtrl.GetSelection()))
        if self.m_surfaceProcessCtrl.GetSelection() == 2:
            form.add_field('cjh', str(self.GetCJH()))
        form.add_field('impendance', str(self.m_impedanceCtrl.GetSelection()))
        form.add_field('bankong', str(self.m_halfHoleCtrl.GetSelection()))
        form.add_field('blind', self.GetBlindValue())
        form.add_field('via_in_pad', self.GetViaInPad())
        form.add_field('test', self.GetTestMethod())
        form.add_field('shipment_report', str(self.m_deliveryReportCtrl.GetSelection()))
        form.add_field('slice_report', str(self.m_analysisReportCtrl.GetSelection()))
        form.add_field('report_type', str(self.GetReportType()))
        form.add_field('beveledge', str(self.m_goldFingerCtrl.GetSelection()))
        form.add_field('review_file', self.GetReviewFile())
        form.add_field('has_period', self.GetHasPeriod())
        if self.m_ulMarkCtrl.GetSelection() != 0:
            form.add_field('period_format', self.GetPeriodFormat())        
        form.add_field('film_report', str(self.m_filmCtrl.GetSelection()))
        form.add_field('pcb_note', self.m_specialRequestsCtrl.GetValue())
        
        form.add_field('region_id', '211') #TODO
        form.add_field('country', '211') #TODO
        form.add_field('express', '31') #TODO
        # form.add_field('express', '0')
        # form.add_field('expresstime', '3-5%20days')
        # form.add_field('calc_type', '0')
        # form.add_field('deltime', '72%20hours')
        # form.add_field('activity_code', '')
        # form.add_field('active', '')
        # form.add_field('history_pcb_order_sn', '0')
        # form.add_field('pbnum', '1')
        # form.add_field('isgerber', '1')
        # form.add_field('thermalc', '')
        # form.add_field('rogers', '')
        # form.add_field('holedensity', '0')
        # form.add_field('cjarea', '0')
        # form.add_field('testpoint', '0')
        # form.add_field('zknum', '0')
        # form.add_field('baobian', '')
        # form.add_field('pcscount', '20')
        # form.add_field('pcb_po_number', '')
        # form.add_field('pcb_note', '')
        # form.add_field('review_file', '0')
        # form.add_field('cross_board', '1')
        # form.add_field('user_stamp', '3')
        # form.add_field('paper', '1')
        # form.add_field('file_standard', '2')
        # form.add_field('acceptance', '1')
        
        self.form = form

    def OnUpdatePrice( self, event ):
        self.GetInfoFromSetting()
        self.form.convert_to_dict()

        self.form.make_result()
        url = 'https://www.nextpcb.com/ajax/valuation'
        req1 = urllib.request.Request(url, data=self.form.form_data)
        fp = urllib.request.urlopen(req1)
        data = fp.read()
        self.m_priceDetailsViewListCtrl.DeleteAllItems()
        encoding = fp.info().get_content_charset('utf-8')
        quote = json.loads(data.decode(encoding))
        # text_file = open("d:\QuotePCB.txt", "w")
        # n = text_file.write(data.decode(encoding))
        # text_file.close()

        if quote['code'] != 200:
            wx.MessageBox(quote['msg'], "Error", wx.OK | wx.ICON_ERROR)
            return

        data = ['Fabrication:', '']
        self.m_priceDetailsViewListCtrl.AppendItem(data)
                
        if 'discount' in quote['data']:
            value = '$' + str(quote['data']['pcb_total_original'])
            data = ['PCB Price', value]
            self.m_priceDetailsViewListCtrl.AppendItem(data)

            value = '$' + str(quote['data']['discount']['pcb']['discount_amount'])
            data =[quote['data']['discount']['pcb']['title'], value]
            self.m_priceDetailsViewListCtrl.AppendItem(data)
        else:
            value = '$' + str(quote['data']['pcb_total'])
            data = ['PCB Price', value]
            self.m_priceDetailsViewListCtrl.AppendItem(data)
        
        #freight_value = quote['data']['freight']
        #data = ['Shipping Cost', value]
        #self.m_priceDetailsViewListCtrl.AppendItem(data)
        #wx.MessageBox(f"freight_value:{freight_value}.total{quote['data']['total']}", "Help", style=wx.ICON_INFORMATION)
        
        value = '$' + str(round(float(quote['data']['total']) - float(quote['data']['freight']), 2))
        data = ['Total', value]
        self.m_priceDetailsViewListCtrl.AppendItem(data)

        value = quote['data']['delivery_date']
        data = ['Delivery Date', value]
        self.m_priceDetailsViewListCtrl.AppendItem(data)

        locale.setlocale(locale.LC_ALL, '')
        deldate = str(quote['data']['delivery_date'][0:10])
        fabDueDate = str((datetime.strptime(deldate, '%Y/%m/%d') - datetime.now()).days)

        value = str(round(quote['data']['weight'], 4)) + 'kg'
        data = ['Weight', value]
        self.m_priceDetailsViewListCtrl.AppendItem(data)

        value = str(round(quote['data']['list']['pcb']['area'] / 10000, 4)) + '㎡'
        data = ['Area', value]
        self.m_priceDetailsViewListCtrl.AppendItem(data)

        data = ['', '']
        self.m_priceDetailsViewListCtrl.AppendItem(data)

        totalPrice = round(float(quote['data']['total']) - float(quote['data']['freight']), 2)
                      
        value = '$' + str(totalPrice)
        data = ['Total Price', value]
        self.m_priceDetailsViewListCtrl.AppendItem(data)
        
        self.m_amountCtrl.SetLabel(str(self.GetPcbQuantity()))
        self.m_priceCtrl.SetLabel(str(totalPrice))
        if self.m_template.GetSelection() == 0:
            self.m_dueDateCtrl.SetLabel(str(self.GetDaysFromString(fabDueDate)))
        else:
            self.m_dueDateCtrl.SetLabel('-')
        
           
    def GetImagePath( self, bitmap_path ):
        return os.path.join(os.path.dirname(__file__), bitmap_path)

    def GetPcbQuantity( self ):
        n = int(self.m_quantityCtrl.GetString(self.m_quantityCtrl.GetSelection()))
        if self.m_pcbPackaingCtrl.GetSelection() == 1 or self.m_pcbPackaingCtrl.GetSelection() == 2:
            return n * int(self.m_panelizeXCtrl.GetValue()) * int(self.m_panelizeYCtrl.GetValue())
        else:
            return n
            
    def GetPcbLength( self ):
        if self.m_pcbPackaingCtrl.GetSelection() == 0:
            if self.m_marginModeCtrl.GetSelection() == 1 or self.m_marginModeCtrl.GetSelection() == 3:
                return float(self.m_sizeXCtrl.GetValue()) + float(self.m_marginValueCtrl.GetValue()) * 2
            else:
                return float(self.m_sizeXCtrl.GetValue())
        else:
            if self.m_marginModeCtrl.GetSelection() == 1 or self.m_marginModeCtrl.GetSelection() == 3:
                return float(self.m_sizeXCtrl.GetValue()) * int(self.m_panelizeXCtrl.GetValue()) + float(self.m_marginValueCtrl.GetValue()) * 2
            else:
                return float(self.m_sizeXCtrl.GetValue()) * int(self.m_panelizeXCtrl.GetValue())
            
    def GetPcbWidth( self ):
        if self.m_pcbPackaingCtrl.GetSelection() == 0:
            if self.m_marginModeCtrl.GetSelection() == 1 or self.m_marginModeCtrl.GetSelection() == 3:
                return float(self.m_sizeYCtrl.GetValue()) + float(self.m_marginValueCtrl.GetValue()) * 2
            else:
                return float(self.m_sizeYCtrl.GetValue())
        else:
            if self.m_marginModeCtrl.GetSelection() == 1 or self.m_marginModeCtrl.GetSelection() == 3:
                return float(self.m_sizeYCtrl.GetValue()) * int(self.m_panelizeYCtrl.GetValue()) + float(self.m_marginValueCtrl.GetValue()) * 2
            else:
                return float(self.m_sizeYCtrl.GetValue()) * int(self.m_panelizeYCtrl.GetValue())

    def GetMarginMode( self ):
        if self.m_marginModeCtrl.GetSelection() == 0:
            return "N/A"
        elif self.m_marginModeCtrl.GetSelection() == 1:
            return "X"
        elif self.m_marginModeCtrl.GetSelection() == 2:
            return "Y"
        elif self.m_marginModeCtrl.GetSelection() == 3:
            return "XY"
        else:
            return "N/A"

    def GetOuterCopperThickness( self ):
        if self.m_outerCopperThicknessCtrl.GetSelection() == 0:
            return 1
        elif self.m_outerCopperThicknessCtrl.GetSelection() == 1:
            return 2
        
    def GetInnerCopperThickness( self ):
        if self.m_innerCopperThicknessCtrl.GetSelection() == 0:
            return 0.5
        if self.m_innerCopperThicknessCtrl.GetSelection() == 1:
            return 1
        elif self.m_innerCopperThicknessCtrl.GetSelection() == 2:
            return 2
        
    def GetMinTraceWidthAndClearance( self ):
        if self.m_minTraceWidthClearanceCtrl.GetSelection() == 0:
            return 10
        elif self.m_minTraceWidthClearanceCtrl.GetSelection() == 1:
            return 8
        elif self.m_minTraceWidthClearanceCtrl.GetSelection() == 2:
            return 6
        elif self.m_minTraceWidthClearanceCtrl.GetSelection() == 3:
            return 5
        elif self.m_minTraceWidthClearanceCtrl.GetSelection() == 4:
            return 4
        elif self.m_minTraceWidthClearanceCtrl.GetSelection() == 5:
            return 3.5
        else:
            return 10
        
    def GetMinHoleSize( self ):
        if self.m_minHoleSizeCtrl.GetSelection() == 0:
            return 0.3
        elif self.m_minHoleSizeCtrl.GetSelection() == 1:
            return 0.25
        elif self.m_minHoleSizeCtrl.GetSelection() == 2:
            return 0.2
        elif self.m_minHoleSizeCtrl.GetSelection() == 3:
            return 0.15
        else:
            return 0.3
        
    def GetCJH( self ):
        if self.m_goldThicknessCtrl.GetSelection() == 0:
            return 1
        elif self.m_goldThicknessCtrl.GetSelection() == 1:
            return 2
        elif self.m_goldThicknessCtrl.GetSelection() == 2:
            return 3
        else:
            return 1
    
    def GetBlindValue( self ):
        if self.m_blindViaCtrl.GetSelection() == 0:
            return "0"
        elif self.m_hdiStructureCtrl.GetSelection() == 0:
            return "1"    
        elif self.m_hdiStructureCtrl.GetSelection() == 1:
            return "2"    
        elif self.m_hdiStructureCtrl.GetSelection() == 2:
            return "3"    
        
    def GetTestMethod( self ):
        if self.m_testMethodCtrl.GetSelection() == 0:
            return 'Sample Test Free'
        elif self.m_testMethodCtrl.GetSelection() == 1:
            return 'Batch Flying Probe Test'
        elif self.m_testMethodCtrl.GetSelection() == 2:
            return 'Batch Fixture Test'
    
    def GetReviewFile( self ):
        if self.m_approveWorkingGerberCtrl.GetSelection() == 0:
            return '0'
        else:
            return '2'
    
    def GetHasPeriod( self ):
        if self.m_ulMarkCtrl.GetSelection() == 0:
            return '2'
        else:
            return '6'
        
    def GetPeriodFormat( self ):
        if self.m_ulMarkCtrl.GetSelection() == 1:
            return '2'
        elif self.m_ulMarkCtrl.GetSelection() == 2:
            return '1'
        
    def GetViaInPad( self ):
        if self.m_padHoleCtrl.GetSelection() == 0:
            return 'N/A'
        else:
            return 'Have'
    
    def GetReportType( self ):
        if self.m_deliveryReportCtrl.GetSelection() == 0 and self.m_analysisReportCtrl.GetSelection() == 0:
            return 0
        elif self.m_reportFormatCtrl.GetSelection() == 0:
            return 2
        elif self.m_reportFormatCtrl.GetSelection() == 1:
            return 1        

    def GetDaysFromString( self, str ):
        numbers = re.findall('\d+', str)
        if '小时' in str:
            return int(int(numbers[0]) / 24)
        else:
            return int(numbers[0])
    
    def SetBoardThickness( self, thickness ):
        for i in range(self.m_boardThicknessCtrl.GetCount()):
            if thickness <= float(self.m_boardThicknessCtrl.GetString(i)):
                self.m_boardThicknessCtrl.SetSelection(i)
                break
 
    def SetMinTrace( self, minTraceWidth, minTraceClearance ):
        if minTraceWidth == 0 and minTraceClearance == 0:
            minTrace = 6
        elif minTraceWidth == 0:
            minTrace = minTraceClearance
        elif minTraceClearance == 0:
            minTrace = minTraceWidth
        else:
            minTrace = min(minTraceWidth, minTraceClearance) 
        
        if minTrace == 0:
            minTrace = 6
            self.m_minTraceWidthClearanceCtrl.SetSelection(2)
        elif minTrace >= 10:
            minTrace = 10
            self.m_minTraceWidthClearanceCtrl.SetSelection(0)
        elif minTrace >= 8:
            minTrace = 8  
            self.m_minTraceWidthClearanceCtrl.SetSelection(1)
        elif minTrace >= 6:
            minTrace = 6
            self.m_minTraceWidthClearanceCtrl.SetSelection(2)
        elif minTrace >= 5:
            minTrace = 5
            self.m_minTraceWidthClearanceCtrl.SetSelection(3)
        elif minTrace >= 4:
            minTrace = 4
            self.m_minTraceWidthClearanceCtrl.SetSelection(4)
        else:
            minTrace = 3.5
            self.m_minTraceWidthClearanceCtrl.SetSelection(5)
   
    def SetMinHole( self, minHoleSize ):
        if minHoleSize == 0:
            minHoleSize = 0.3
            self.m_minHoleSizeCtrl.SetSelection(0)
        elif minHoleSize >= 0.3:
            minHoleSize = 0.3
            self.m_minHoleSizeCtrl.SetSelection(0)
        elif minHoleSize >= 0.25:
            minHoleSize = 0.25
            self.m_minHoleSizeCtrl.SetSelection(1)
        elif minHoleSize >= 0.2:
            minHoleSize = 0.2
            self.m_minHoleSizeCtrl.SetSelection(2)
        else:
            minHoleSize = 0.15
            self.m_minHoleSizeCtrl.SetSelection(3)

    def SetSMTInfo( self ):
        smtPadCount = 0
        topSMT = False
        bottomSMT = False
        footprints = list(self.board.GetFootprints())
        footprints.sort(key=lambda x: x.GetReference())
        footprintReferecens = defaultdict(int)
        for i, footprint in enumerate(footprints):
            if footprint.GetAttributes() & pcbnew.FP_SMD == pcbnew.FP_SMD:
            # if not footprint.HasThroughHolePads():
                if footprint.GetLayer() == pcbnew.F_Cu:
                    topSMT = True
                elif footprint.GetLayer() == pcbnew.B_Cu:
                    bottomSMT = True
                footprintReferecens[str(footprint.GetFPID().GetLibItemName()) + '&&&&' + footprint.GetValue().upper()] += 1
                smtPadCount += len(footprint.Pads())
                # pads = list(footprint.Pads())
                # for pad in pads:
                #     if pad.ShowPadAttr() == 'SMD':
                #         if pad.IsOnLayer(pcbnew.F_Cu) or pad.IsOnLayer(pcbnew.B_Cu):
                #             smtPadCount = smtPadCount + 1
                                
        # self.m_smtSingleDouleSideCtrl.SetSelection(1 if topSMT and bottomSMT else 0)
        # self.m_smtComponentKindsCtrl.SetValue(str(len(footprintReferecens.items())))
        # self.m_smtPadCountCtrl.SetValue(str(smtPadCount))

    def generate_fabrication_data(self, e):
        """Generate fabrication data."""
        self.fabrication.fill_zones()
        self.fabrication.generate_geber(None)
        self.fabrication.generate_excellon()
        self.fabrication.zip_gerber_excellon()


    def OnPlaceOrder(self, e):
        self.m_placeOrderButton.Enabled = False
        try:
            wx.BeginBusyCursor()
            self.init_fabrication()
            self.generate_fabrication_data(e)
            self.place_order_request()
        finally:
            wx.EndBusyCursor()
            self.m_placeOrderButton.Enabled = True

    def place_order_request(self):
        zipname = f"GERBER-{self.fabrication.filename.split('.')[0]}.zip"
        zipfile = os.path.join(self.fabrication.outputdir, zipname)
        files = {'file': open(zipfile, 'rb')}
        upload_url = "https://www.nextpcb.com/Upfile/kiCadUpFile"
        self.GetInfoFromSetting()
        self.form.add_field('type', 'pcbfile')
        self.form.convert_to_dict()
        self.form.form_dict['blength'] = str(round(self.GetPcbLength(), 2))
        self.form.form_dict['bwidth'] = str(round(self.GetPcbWidth(), 2))
        rsp = requests.post(
            upload_url,
            files=files,
            data=self.form.form_dict
        )
        urls = json.loads(rsp.content)
        uat_url = str(urls['redirect'])
        webbrowser.open(uat_url)

    # def SetDIPInfo( self ):
    #     dipPadCount = 0
    #     footprints = list(self.board.GetFootprints())
    #     footprints.sort(key=lambda x: x.GetReference())
    #     footprintReferecens = defaultdict(int)
    #     for i, footprint in enumerate(footprints):
    #         if footprint.GetAttributes() & pcbnew.FP_THROUGH_HOLE == pcbnew.FP_THROUGH_HOLE:
    #         # if footprint.HasThroughHolePads():
    #             footprintReferecens[str(footprint.GetFPID().GetLibItemName()) + '&&&&' + footprint.GetValue().upper()] += 1
    #             dipPadCount += len(footprint.Pads())
                
    #     self.m_doDIPCtrl.SetSelection(1 if dipPadCount > 0 else 0)
    #     self.m_dipComponentKindsCtrl.SetValue(str(len(footprintReferecens.items())))
    #     self.m_dipPadCountCtrl.SetValue(str(dipPadCount))
    #     self.OnDoDIPChanged(None)

