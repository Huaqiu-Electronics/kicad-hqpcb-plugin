import os
from pcbnew import ActionPlugin
from kicad_amf_plugin.kicad_nextpcb_new.nextpcb_plugin._main import _main


class NextPcbBomTool(ActionPlugin):
    def defaults(self):
        self.name = "NextPCB Tools"
        self.category = "Fabrication data generation"
        self.description = (
            "Generate NextPCB-compatible Gerber, Excellon, BOM and CPL files"
        )
        self.show_toolbar_button = True
        path, filename = os.path.split(os.path.abspath(__file__))
        self.icon_file_name = os.path.join(path, "nextPCB-icon.png")
        self._pcbnew_frame = None

    def Run(self):
        _main()
