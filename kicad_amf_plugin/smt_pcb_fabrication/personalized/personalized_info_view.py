import wx
from kicad_amf_plugin.order.order_region import OrderRegion, SupportedRegion
from kicad_amf_plugin.settings.setting_manager import SETTING_MANAGER
from kicad_amf_plugin.settings.form_value_fitter import fitter_and_map_form_value
from .personalized_info_model import PersonalizedInfoModel
from .ui_smt_personalized import UiPersonalizedService, BOX_SP_REQUEST
from kicad_amf_plugin.utils.constraint import BOOLEAN_CHOICE
from .personalized_info_model import PersonalizedInfoModel
from kicad_amf_plugin.utils.form_panel_base import FormKind, FormPanelBase
from kicad_amf_plugin.utils.roles import EditDisplayRole
from kicad_amf_plugin.settings.single_plugin import SINGLE_PLUGIN

ASSEMBLY_WELD ={
    _("No Need"): "No Need",
    _("Need"): "Need",
}

LAYOUT_CLEANING = {
    _("General Cleaning"): "General Cleaning",
    _("Precision Cleaning"): "Precision Cleaning",
}

MATERIAL_BAKING = {
    _("No Need"): "No Need",
    _("Need"): "Need",
}

WELDING_WIRE = {
    _("No Need"): "No Need",
    _("Need"): "Need",
}

IS_TEST = {
    _("No Need"): "No Need",
    _("Need"): "Need",
}

IS_ASSEMBLE = {
    _("No Need"): "No Need",
    _("Need"): "Need",    
}

PROGRAM_BURNING = {
    _("No Need"): "No Need",
    _("Need"): "Need",
}

NEED_SPLIT = {
    _("No Need"): "No Need",
    _("Need"): "Need",
}

INCREASE_TINNING = {
    _("No Need"): "No Need",
    _("Need"): "Need",
}

NEED_CONFORMAL_COATING = {
    _("No Need"): "No Need",
    _("Single Side"): "Single Side",
    _("Double Side"): "Double Side",
}

FIRST_CONFIRM = {
    _("No Need"): "No Need",
    _("Need"): "Need",
}

PACKING_TYPE = {
    _("Bubble Wrap"): "Bubble Wrap",
    _("Anti-static and Bubble Bag"): "Anti-static and Bubble Bag",
    _("Electrostatic Bag with Knife Card"): "Electrostatic Bag with Knife Card",
}


class SmtPersonalizedInfoView(UiPersonalizedService, FormPanelBase):
    def __init__(self, parent, _):
        super().__init__(parent)
        self.special_process: PersonalizedInfoModel = None
        self.initUI()
        
        self.need_split.Bind(wx.EVT_CHOICE, self.on_need_split_changed)

    def initUI(self):
        # NOTE It seems that all tests are free now
        self.solder_paste_type.Append( _("Lead-free Technology") )
        self.solder_paste_type.SetSelection(0)
        self.is_assembly_weld.Append( [i for i in ASSEMBLY_WELD] )
        self.is_assembly_weld.SetSelection(0)
        self.is_layout_cleaning.Append( [i for i in LAYOUT_CLEANING] )
        self.is_layout_cleaning.SetSelection(0)
        self.is_material_baking.Append( [i for i in MATERIAL_BAKING] )
        self.is_material_baking.SetSelection(0)
        self.is_welding_wire.Append( [i for i in WELDING_WIRE] )
        self.is_welding_wire.SetSelection(0)
        self.is_test.Append( [i for i in IS_TEST] )
        self.is_test.SetSelection(0)
        self.is_assemble.Append( [i for i in IS_ASSEMBLE] )
        self.is_assemble.SetSelection(0)
        self.is_program_burning.Append( [i for i in PROGRAM_BURNING] )
        self.is_program_burning.SetSelection(0)
        self.need_split.Append( [i for i in NEED_SPLIT] )
        self.need_split.SetSelection(0)
        self.is_increase_tinning.Append( [i for i in INCREASE_TINNING] )
        self.is_increase_tinning.SetSelection(0)
        self.need_conformal_coating.Append( [i for i in NEED_CONFORMAL_COATING] )
        self.need_conformal_coating.SetSelection(0)
        self.is_first_confirm.Append( [i for i in FIRST_CONFIRM] )
        self.is_first_confirm.SetSelection(0)
        self.packing_type.Append( [i for i in PACKING_TYPE] )
        self.packing_type.SetSelection(0)

        self.x_ray_number.SetValue("1")
        self.x_ray_unit_number.SetValue("1")
        self.single_pcb_width.SetValue("")
        self.single_pcb_height.SetValue("")
        self.on_region_changed()

    @fitter_and_map_form_value
    def get_from(self, kind: FormKind) -> "dict":
        info = PersonalizedInfoModel(
            
            solder_paste_type = self.solder_paste_type.GetSelection(),
            is_assembly_weld = self.is_assembly_weld.GetSelection(),
            is_layout_cleaning = self.is_layout_cleaning.GetSelection(),
            is_material_baking = self.is_material_baking.GetSelection(),
            is_welding_wire = self.is_welding_wire.GetSelection(),
            is_test = self.is_test.GetSelection(),
            is_assemble = self.is_assemble.GetSelection(),
            is_program_burning = self.is_program_burning.GetSelection(),
            need_split = self.need_split.GetSelection(),
            is_increase_tinning = self.is_increase_tinning.GetSelection(),
            need_conformal_coating = self.need_conformal_coating.GetSelection(),
            is_first_confirm = self.is_first_confirm.GetSelection(),
            packing_type = self.packing_type.GetSelection(),
            
            x_ray_number = self.x_ray_number.GetValue(),
            x_ray_unit_number = self.x_ray_unit_number.GetValue(),
            

        )
        pcb_width_str = self.single_pcb_width.GetValue()
        pcb_height_str = self.single_pcb_height.GetValue()
        if pcb_width_str == '' or pcb_height_str == '':
            info.pcb_width = pcb_width_str
            info.pcb_height = pcb_height_str
        else:
            info.pcb_width = str(float(pcb_width_str) * 0.1)
            info.pcb_height = str(float(pcb_height_str) * 0.1)
        return vars(info)

    @property
    def sp_box(self):
        return self.FindWindowById(BOX_SP_REQUEST)

    def on_need_split_changed( self, evt=None ):
        self.single_pcb_panel.Show(self.need_split.GetSelection() == 1)  
        self.Layout()
        if SINGLE_PLUGIN.get_main_wind() is not None:
            SINGLE_PLUGIN.get_main_wind().smt_adjust_size()

    def on_region_changed(self):
        for i in [ self.is_layout_cleaning, self.is_layout_cleaning_label,
                  self.is_welding_wire, self.is_welding_wire_label, self.is_assemble, self.is_assemble_label,
                  self.is_increase_tinning , self.is_increase_tinning_label,] :
            i.Show( SETTING_MANAGER.order_region == SupportedRegion.CHINA_MAINLAND )
        
        self.need_split.SetSelection(0)
        self.need_split.Enable(SETTING_MANAGER.order_region == SupportedRegion.CHINA_MAINLAND)
        self.on_need_split_changed( None )
        self.Layout()


