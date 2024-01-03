from kicad_amf_plugin.kicad.board_manager import BoardManager
from kicad_amf_plugin.pcb_fabrication.special_process.ui_special_process import UiSpecialProcess
from kicad_amf_plugin.utils.form_panel_base import FormKind, FormPanelBase


class SpecialProcessSmtView(UiSpecialProcess, FormPanelBase):
    def __init__(self, parent, board_manager: BoardManager):
        super().__init__(parent)
        self.board_manager = board_manager