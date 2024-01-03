from kicad_amf_plugin.pcb_fabrication.personalized.ui_personalized import UiPersonalizedService, BOX_SP_REQUEST
from kicad_amf_plugin.utils.form_panel_base import FormKind, FormPanelBase

class PersonalizedSmtView(UiPersonalizedService, FormPanelBase):
    def __init__(self, parent, _):
        super().__init__(parent)
        # self.special_process: PersonalizedInfoModel = None