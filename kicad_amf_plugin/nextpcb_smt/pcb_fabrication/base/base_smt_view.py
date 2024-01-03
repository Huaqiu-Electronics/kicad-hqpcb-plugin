from kicad_amf_plugin.pcb_fabrication.base.ui_base_info import (
        UiBaseInfo, BOX_SIZE_SETTING,
        BOX_PANEL_SETTING, BOX_BREAK_AWAY, )
from kicad_amf_plugin.utils.form_panel_base import FormKind, FormPanelBase
from kicad_amf_plugin.kicad.board_manager import BoardManager


class BaseSmtView(UiBaseInfo, FormPanelBase):
    def __init__(self, parent, board_manager: BoardManager):
        super().__init__(parent)
        self.board_manager = board_manager
        
        