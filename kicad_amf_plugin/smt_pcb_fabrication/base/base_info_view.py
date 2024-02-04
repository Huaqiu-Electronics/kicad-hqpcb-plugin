from kicad_amf_plugin.kicad.board_manager import BoardManager
from kicad_amf_plugin.order.supported_region import SupportedRegion
from kicad_amf_plugin.settings.setting_manager import SETTING_MANAGER
from kicad_amf_plugin.settings.single_plugin import SINGLE_PLUGIN
from kicad_amf_plugin.utils.form_panel_base import FormKind, FormPanelBase
from .base_info_model import BaseInfoModel
from kicad_amf_plugin.gui.event.pcb_fabrication_evt_list import (
    LayerCountChange, boardCount,EVT_BOARD_COUNT )
from .ui_base_info import (
    UiBaseInfo,
    BOX_SIZE_SETTING,
    # BOX_PANEL_SETTING,
    # BOX_BREAK_AWAY,
)
from kicad_amf_plugin.utils.validators import (
    NumericTextCtrlValidator,
    FloatTextCtrlValidator,
)
from kicad_amf_plugin.utils.roles import EditDisplayRole
from kicad_amf_plugin.settings.form_value_fitter import fitter_and_map_form_value
from kicad_amf_plugin.settings.supported_layer_count import AVAILABLE_LAYER_COUNTS
from kicad_amf_plugin.gui.event.pcb_fabrication_evt_list import ( ComboNumber )

import pcbnew
import wx
from wx.lib.pubsub import pub



AVAILABLE_MATERIAL_TYPES = [
    EditDisplayRole(1, _("Industrial Control Electronics")),
    EditDisplayRole(2, _("Automotive Electronics")),
    EditDisplayRole(3, _("Medical Electronics")),
    EditDisplayRole(4, _("New Energy Electronics")),
    EditDisplayRole(5, _("Military Electronics")),
    EditDisplayRole(6, _("Consumer Electronics")),
]



PCB_SOFT_BOARD = [
    EditDisplayRole(0, _("Hard Board")),
    EditDisplayRole(1, _("Soft Board")),
    EditDisplayRole(2, _("Combination of Hoft and Hard")),
]


SINGLE_DOUBLE_TECHNIQUE = [
    EditDisplayRole(1, _("Single Side")),
    EditDisplayRole(2, _("Double Side")),
]

AVAILABLE_QUANTITY = [
    5,
    10,
    15,
    20,
    25,
    30,
    40,
    50,
    75,
    100,
    125,
    150,
    200,
    250,
    300,
    350,
    400,
    450,
    500,
    600,
    700,
    800,
    900,
    1000,
    1500,
    2000,
    2500,
    3000,
    3500,
    4000,
    4500,
    5000,
    5500,
    6000,
    6500,
    7000,
    7500,
    8000,
    9000,
    10000,
]
 
class SmtBaseInfoView(UiBaseInfo, FormPanelBase):
    def __init__(self, parent, board_manager: BoardManager):
        super().__init__(parent)
        self.board_manager = board_manager
        
        self.combo_number.Bind(wx.EVT_TEXT, self.on_combo_number_change)

        # self.combo_pcb_package_kind.Bind(wx.EVT_CHOICE, self.on_pcb_packaging_changed)
        # self.comb_margin_mode.Bind(wx.EVT_CHOICE, self.on_margin_mode_changed)
        # self.combo_layer_count.Bind(wx.EVT_CHOICE, self.on_layer_count_changed)
        # self.combo_number.Bind(wx.EVT_CHOICE, self.on_choice)
        # for editor in self.edit_panel_x, self.edit_panel_y:
        #     editor.SetValidator(NumericTextCtrlValidator())
        # self.edit_margin_size.SetValidator(FloatTextCtrlValidator())


    @property
    def box_piece_or_panel_size(self):
        return self.FindWindowById(BOX_SIZE_SETTING)


    def get_pcb_length(self):
        """Default is mm


        Returns:
            _type_: float
        """
        return float(self.edit_size_x.GetValue())
        

    def get_pcb_width(self):
        """Default is mm


        Returns:
            _type_: float
        """
        return float(self.edit_size_y.GetValue())

    @fitter_and_map_form_value
    def get_from(self, kind: FormKind) -> "dict":
        data = BaseInfoModel(
            
            application_sphere =AVAILABLE_MATERIAL_TYPES[ self.application_sphere.GetSelection() ].EditRole,
            is_pcb_soft_board= PCB_SOFT_BOARD[ self.is_pcb_soft_board.GetSelection() ].EditRole,
            single_or_double_technique= SINGLE_DOUBLE_TECHNIQUE[ self.single_or_double_technique.GetSelection() ].EditRole,
            number=self.combo_number.GetValue(),
            pcb_ban_height=str(
                FormPanelBase.convert_geometry(
                    kind, SETTING_MANAGER.order_region, self.get_pcb_length()
                )
            ),
            pcb_ban_width=str(
                FormPanelBase.convert_geometry(
                    kind, SETTING_MANAGER.order_region, self.get_pcb_width()
                )
            ),
        )
        return vars(data)

    def init(self):
        self.initUI()
        self.loadBoardInfo()

    def getBaseInfo(self):
        return self.base_info

    def initUI(self):
        
        self.application_sphere.Append([i.DisplayRole for i in AVAILABLE_MATERIAL_TYPES])
        self.application_sphere.SetSelection(0)
        
        self.is_pcb_soft_board.Append([i.DisplayRole for i in PCB_SOFT_BOARD])
        self.is_pcb_soft_board.SetSelection(0)
        
        self.single_or_double_technique.Append([i.DisplayRole for i in SINGLE_DOUBLE_TECHNIQUE])
        self.single_or_double_technique.SetSelection(1)
        
        self.combo_number.SetValue("5")        
        for i in self.edit_size_x, self.edit_size_y:
            i.SetEditable(False)


    def loadBoardInfo(self):
        boardWidth = pcbnew.ToMM(
            self.board_manager.board.GetBoardEdgesBoundingBox().GetWidth()
        )
        boardHeight = pcbnew.ToMM(
            self.board_manager.board.GetBoardEdgesBoundingBox().GetHeight()
        )
        self.edit_size_x.SetValue(str(boardWidth))
        self.edit_size_y.SetValue(str(boardHeight))

    def on_combo_number_change(self, evt):
        new_number = self.combo_number.GetValue()
        pub.sendMessage("combo_number", param1=new_number)


    def on_region_changed(self):
        # pass
        for i in [self.application_sphere , self.application_sphere_label,   
                self.is_pcb_soft_board ,self.is_pcb_soft_board_label
                ]:
            i.Show(SETTING_MANAGER.order_region == SupportedRegion.CHINA_MAINLAND)
        self.Layout()
