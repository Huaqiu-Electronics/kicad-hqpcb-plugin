from kicad_amf_plugin.kicad.board_manager import BoardManager
from kicad_amf_plugin.settings.form_value_fitter import fitter_and_map_form_value
from .process_info_model import ProcessInfoModel
from kicad_amf_plugin.utils.form_panel_base import FormKind, FormPanelBase
from kicad_amf_plugin.utils.roles import EditDisplayRole
from kicad_amf_plugin.settings.setting_manager import SETTING_MANAGER
from kicad_amf_plugin.settings.single_plugin import SINGLE_PLUGIN
from kicad_amf_plugin.order.supported_region import SupportedRegion

from .ui_process_info import UiProcessInfo
import wx


IS_PLUG = [
    EditDisplayRole(0, _("No")),
    EditDisplayRole(1, _("Yes")),

]

STEEL_TYPE = [
    EditDisplayRole(0, _("Ordinary Steel Mesh")),
    EditDisplayRole(1, _("Stepped Steel Mesh")),
]


STEEL_FOLLOW_DELIVERY = [
    EditDisplayRole(0, _("No Need")),
    EditDisplayRole(1, _("Need")),
]


class SmtProcessInfoView(UiProcessInfo, FormPanelBase):
    def __init__(self, parent, board_manager: BoardManager):
        super().__init__(parent)
        self.board_manager = board_manager

        self.Fit()
        # self.judge_plug()
        self.is_plug.Bind(wx.EVT_CHOICE, self.judge_plug)
        

    @fitter_and_map_form_value
    def get_from(self, kind: FormKind) -> "dict":
        info = ProcessInfoModel(
            bom_material_type_number= self.bom_material_type_number.GetValue(),
            patch_pad_number = self.patch_pad_number.GetValue(),
            is_plug = IS_PLUG[self.is_plug.GetSelection()].EditRole,
            # self.is_plug.GetStringSelection(),
            plug_number = self.plug_number.GetValue(),
            steel_type = STEEL_TYPE[self.steel_type.GetSelection()].EditRole, 
            is_steel_follow_delivery = STEEL_FOLLOW_DELIVERY[  self.is_steel_follow_delivery.GetSelection()].EditRole, 

        )
        return vars(info)

    def init(self):
        self.initUI()

    def initUI(self):
        self.is_plug.Append( [i.DisplayRole for i in IS_PLUG] )
        self.is_plug.SetSelection(1)
 
        self.steel_type.Append( [i.DisplayRole for i in STEEL_TYPE] )
        self.steel_type.SetSelection(0)
 
        self.is_steel_follow_delivery.Append( [i.DisplayRole for i in STEEL_FOLLOW_DELIVERY] )
        self.is_steel_follow_delivery.SetSelection(0)
        
        self.bom_material_type_number.SetValue("1")
        self.patch_pad_number.SetValue("1")
        self.plug_number.SetValue("1")


    def on_region_changed(self):
        for i in self.is_steel_follow_delivery, self.is_steel_follow_delivery_label:
            i.Show(SETTING_MANAGER.order_region == SupportedRegion.CHINA_MAINLAND)
        self.Layout()

    def judge_plug(self,evt=None):
        judge_plug = self.is_plug.GetSelection()
        print(f"--judge_plug---{judge_plug}")
        # if judge_plug == "0":
        for i in self.plug_number, self.plug_number_label :
            i.Show( self.is_plug.GetSelection() != 0 )
        self.Layout()
        SINGLE_PLUGIN.get_main_wind().smt_adjust_size()

