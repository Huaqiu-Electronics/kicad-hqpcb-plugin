from .ui_region_select import UiRegionSelect
from kicad_amf_plugin.utils.form_panel_base import FormKind, FormPanelBase

from kicad_amf_plugin.order.supported_region import SupportedRegion
from kicad_amf_plugin.utils.roles import EditDisplayRole
from kicad_amf_plugin.settings.setting_manager import SETTING_MANAGER

OrderRegionSettings = (
    EditDisplayRole(SupportedRegion.CHINA_MAINLAND, _("Mainland China")),
    EditDisplayRole(SupportedRegion.EUROPE_USA, _("Worldwide (English)")),
    EditDisplayRole(SupportedRegion.JAPAN, _("Worldwide (Japanese)")),
)

class RegionSelectView( UiRegionSelect, FormPanelBase ):
    def __init__(self,  *args, **kw):
        super().__init__( *args, **kw)
        
        self.choice_order_region.AppendItems(
            [i.DisplayRole for i in OrderRegionSettings]
        )
        self.choice_order_region.SetSelection(SETTING_MANAGER.order_region)
