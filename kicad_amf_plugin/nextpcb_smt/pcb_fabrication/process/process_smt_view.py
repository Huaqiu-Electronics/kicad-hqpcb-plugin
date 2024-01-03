from kicad_amf_plugin.pcb_fabrication.process.ui_process_info import UiProcessInfo
from kicad_amf_plugin.kicad.board_manager import BoardManager
from kicad_amf_plugin.utils.form_panel_base import FormKind, FormPanelBase

import wx


class ProcessSmtView(UiProcessInfo, FormPanelBase):
    def __init__(self, parent, board_manager: BoardManager):
        super().__init__(parent)
        