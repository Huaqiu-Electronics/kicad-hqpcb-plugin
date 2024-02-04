from kicad_amf_plugin.kicad.board_manager import BoardManager
from kicad_amf_plugin.settings.form_value_fitter import fitter_and_map_form_value
from .process_info_model import ProcessInfoModel
from kicad_amf_plugin.utils.form_panel_base import FormKind, FormPanelBase
from kicad_amf_plugin.utils.roles import EditDisplayRole
from kicad_amf_plugin.settings.setting_manager import SETTING_MANAGER
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
        # self.loadBoardInfo()

    def initUI(self):
        self.is_plug.Append( [i.DisplayRole for i in IS_PLUG] )
        self.is_plug.SetSelection(0)
 
        self.steel_type.Append( [i.DisplayRole for i in STEEL_TYPE] )
        self.steel_type.SetSelection(0)
 
        self.is_steel_follow_delivery.Append( [i.DisplayRole for i in STEEL_FOLLOW_DELIVERY] )
        self.is_steel_follow_delivery.SetSelection(0)
        
        self.bom_material_type_number.SetValue("1")
        self.patch_pad_number.SetValue("1")
        self.plug_number.SetValue("1")

        
    def loadBoardInfo(self):
        for i in self.label_immersion_gold, self.combo_gold_thickness:
            i.Show(False)

        self.combo_inner_copper_thickness.Enabled = self.layer_count > 2
        self.setup_board_thickness_choice(self.layer_count)
        self.setup_trace_and_via()


    def on_region_changed(self):
        for i in self.is_steel_follow_delivery, self.is_steel_follow_delivery_label:
            i.Show(SETTING_MANAGER.order_region == SupportedRegion.CHINA_MAINLAND)
        self.Layout()
