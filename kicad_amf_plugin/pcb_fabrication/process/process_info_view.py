from kicad_amf_plugin.kicad.board_manager import BoardManager
from kicad_amf_plugin.settings.form_value_fitter import fitter_and_map_form_value
from .process_info_model import ProcessInfoModel
from kicad_amf_plugin.utils.form_panel_base import FormKind, FormPanelBase


from .ui_process_info import UiProcessInfo
import wx
import pcbnew
from pcbnew import PCB_TRACK, PCB_TRACE_T, PCB_ARC_T, PCB_VIA_T


THICKNESS_SETTING = {
    "1": ["0.6", "0.8", "1.0", "1.2", "1.6"],
    "2": ["0.6", "0.8", "1.0", "1.2", "1.6"],
    "4": ["0.6", "0.8", "1.0", "1.2", "1.6", "2.0", "2.5"],
    "6": ["1.0", "1.2", "1.6", "2.0", "2.5"],
    "8": ["1.2", "1.6", "2.0", "2.5"],
    "10": ["1.2", "1.6", "2.0", "2.5"],
    "12": ["1.6", "2.0", "2.5"],
    "14": ["1.6", "2.0", "2.5", "3.0"],
    "16": ["2.0", "2.5", "3.0"],
    "18": ["2.0", "2.5", "3.0", "3.2"],
    "20": ["2.0", "2.5", "3.0", "3.2"],
}

OZ = "oz"

OUTER_THICKNESS_CHOICE = [1, 2]


INNER_COPPER_THICKNESS_CHOICE = [0.5, 1, 2]

MIL = "mil"

MIN_TRACE_WIDTH_CLEARANCE_CHOICE = [10, 8, 6, 5, 4, 3.5]
MIN_HOLE_SIZE_CHOICE = [0.3, 0.25, 0.2, 0.15]

MM = "mm"

DEFAULT_MIN_TRACK_WIDTH = 6

KNOW_COLOR_MAPPING = {
    _("Green"): "Green",
    _("Red"): "Red",
    _("Yellow"): "Yellow",
    _("Blue"): "Blue",
    _("White"): "White",
    _("Matte Black"): "Matte Black",
    _("Black"): "Black",
}

SOLDER_COLOR_CHOICE = [
    _("Green"),
    _("Red"),
    _("Yellow"),
    _("Blue"),
    _("White"),
    _("Matte Black"),
    _("Black"),
]


SOLDER_COVER_CHOICE = {
    _("Tenting Vias"): "Tenting Vias",
    _("Vias not covered"): "Vias not covered",
    _("Solder Mask Plug (IV-B)"): "Solder Mask Plug (IV-B)",
    _("Non-Conductive Fill"): "Non-Conductive Fill & Cap (VII)",
}

SURFACE_PROCESS_CHOICE = {
    _("HASL"): "HASL",
    _("Lead free HASL"): "Lead free HASL",
    _("ENIG"): "ENIG",
    _("OSP"): "OSP",
}

GOLD_THICKNESS_CHOICE = [1, 2, 3]

GOLD_THICKNESS_CHOICE_UNIT = "µm"

SILK_SCREEN_COLOR_BY_SOLDER_COLOR = {
    _("Green"): [_("White")],
    _("Red"): [_("White")],
    _("Yellow"): [_("White")],
    _("Blue"): [_("White")],
    _("White"): [_("Black")],
    _("Matte Black"): [_("White")],
    _("Black"): [_("White")],
}


class ProcessInfoView(UiProcessInfo, FormPanelBase):
    def __init__(self, parent, board_manager: BoardManager):
        super().__init__(parent)
        self.board_manager = board_manager

        self.combo_surface_process.Bind(wx.EVT_CHOICE, self.on_surface_process_changed)
        self.combo_solder_color.Bind(wx.EVT_CHOICE, self.OnMaskColorChange)

        self.Fit()

    @fitter_and_map_form_value
    def get_from(self, kind: FormKind) -> "dict":
        info = ProcessInfoModel(
            bheight=self.combo_board_thickness.GetStringSelection(),
            copper=str(
                self.combo_outer_copper_thickness.GetStringSelection()
            ).removesuffix(OZ),
            lineweight=str(
                self.combo_min_trace_width_clearance.GetStringSelection()
            ).split("/")[0],
            vias=str(self.combo_min_hole_size.GetStringSelection()).removesuffix(MM),
            color=KNOW_COLOR_MAPPING[self.combo_solder_color.GetStringSelection()],
            charcolor=KNOW_COLOR_MAPPING[
                self.combo_silk_screen_color.GetStringSelection()
            ],
            cover=SOLDER_COVER_CHOICE[self.combo_solder_cover.GetStringSelection()],
            spray=SURFACE_PROCESS_CHOICE[
                self.combo_surface_process.GetStringSelection()
            ],
        )
        if self.layer_count > 2:
            info.insidecopper = str(
                self.combo_inner_copper_thickness.GetStringSelection()
            ).removesuffix(OZ)
        if self.combo_surface_process.GetCurrentSelection() == 2:
            info.cjh = str(self.combo_gold_thickness.GetCurrentSelection() + 1)
        return vars(info)

    def init(self):
        self.initUI()
        self.loadBoardInfo()

    def initUI(self):
        self.combo_board_thickness.Append(THICKNESS_SETTING["1"])
        self.combo_board_thickness.SetSelection(4)

        self.combo_outer_copper_thickness.Append(
            [f"{i}{OZ}" for i in OUTER_THICKNESS_CHOICE]
        )
        self.combo_outer_copper_thickness.SetSelection(0)

        self.combo_inner_copper_thickness.Append(
            [f"{i}{OZ}" for i in INNER_COPPER_THICKNESS_CHOICE]
        )
        self.combo_inner_copper_thickness.SetSelection(0)

        self.combo_min_trace_width_clearance.Append(
            [f"{i}/{i}{MIL}" for i in MIN_TRACE_WIDTH_CLEARANCE_CHOICE]
        )
        self.combo_min_trace_width_clearance.SetSelection(2)

        self.combo_min_hole_size.Append([f"{i}{MM}" for i in MIN_HOLE_SIZE_CHOICE])
        self.combo_min_hole_size.SetSelection(0)

        self.combo_solder_color.Append(SOLDER_COLOR_CHOICE)
        self.combo_solder_color.SetSelection(0)

        self.combo_silk_screen_color.Append(
            SILK_SCREEN_COLOR_BY_SOLDER_COLOR[
                self.combo_solder_color.GetStringSelection()
            ]
        )
        self.combo_silk_screen_color.SetSelection(0)

        self.combo_solder_cover.Append([i for i in SOLDER_COVER_CHOICE])
        self.combo_solder_cover.SetSelection(0)

        self.combo_surface_process.Append([i for i in SURFACE_PROCESS_CHOICE])
        self.combo_surface_process.SetSelection(0)

        self.combo_gold_thickness.Append(
            [f"{i}{GOLD_THICKNESS_CHOICE_UNIT}" for i in GOLD_THICKNESS_CHOICE]
        )
        self.combo_gold_thickness.SetSelection(0)

    @property
    def layer_count(self):
        return self.board_manager.board.GetCopperLayerCount()

    def get_board_thickness_in_kicad_setting(self):
        return self.board_manager.board.GetDesignSettings().GetBoardThickness()

    def loadBoardInfo(self):
        for i in self.label_immersion_gold, self.combo_gold_thickness:
            i.Show(False)

        self.combo_inner_copper_thickness.Enabled = self.layer_count > 2
        self.setup_board_thickness_choice(self.layer_count)
        self.setup_trace_and_via()

    def setup_board_thickness_choice(self, event):
        layer_count = event if isinstance(event, int) else event.GetInt()
        self.combo_board_thickness.Clear()
        val_list = THICKNESS_SETTING[str(layer_count)]
        self.combo_board_thickness.Append(val_list)
        self.set_board_thickness(
            pcbnew.ToMM(self.get_board_thickness_in_kicad_setting())
        )

    def on_surface_process_changed(self, evt=None):
        for i in self.label_immersion_gold, self.combo_gold_thickness:
            i.Show(self.combo_surface_process.GetSelection() == 2)
        self.Layout()
        self.Parent.Layout()

    def set_board_thickness(self, thickness):
        for i in range(self.combo_board_thickness.GetCount()):
            if thickness <= float(self.combo_board_thickness.GetString(i)):
                self.combo_board_thickness.SetSelection(i)
                break

    def set_min_trace(self, minTraceWidth, minTraceClearance):
        if minTraceWidth == 0 and minTraceClearance == 0:
            minTrace = 6
        elif minTraceWidth == 0:
            minTrace = minTraceClearance
        elif minTraceClearance == 0:
            minTrace = minTraceWidth
        else:
            minTrace = min(minTraceWidth, minTraceClearance)

        if minTrace == 0:
            minTrace = 6
            self.combo_min_trace_width_clearance.SetSelection(2)
        elif minTrace > 8:
            minTrace = 10
            self.combo_min_trace_width_clearance.SetSelection(0)
        elif minTrace > 6:
            minTrace = 8
            self.combo_min_trace_width_clearance.SetSelection(1)
        elif minTrace > 5:
            minTrace = 6
            self.combo_min_trace_width_clearance.SetSelection(2)
        elif minTrace > 4:
            minTrace = 5
            self.combo_min_trace_width_clearance.SetSelection(3)
        elif minTrace > 3.5:
            minTrace = 4
            self.combo_min_trace_width_clearance.SetSelection(4)
        else:
            minTrace = 3.5
            self.combo_min_trace_width_clearance.SetSelection(5)

    def set_min_hole(self, minHoleSize):
        if minHoleSize == 0:
            minHoleSize = 0.3
            self.combo_min_hole_size.SetSelection(0)
        elif minHoleSize >= 0.3:
            minHoleSize = 0.3
            self.combo_min_hole_size.SetSelection(0)
        elif minHoleSize >= 0.25:
            minHoleSize = 0.25
            self.combo_min_hole_size.SetSelection(1)
        elif minHoleSize >= 0.2:
            minHoleSize = 0.2
            self.combo_min_hole_size.SetSelection(2)
        else:
            minHoleSize = 0.15
            self.combo_min_hole_size.SetSelection(3)

    def OnMaskColorChange(self, event):
        self.combo_silk_screen_color.Clear()
        self.combo_silk_screen_color.Append(
            SILK_SCREEN_COLOR_BY_SOLDER_COLOR[
                self.combo_solder_color.GetStringSelection()
            ]
        )
        self.combo_silk_screen_color.SetSelection(0)

    def on_region_changed(self):
        pass

    def setup_trace_and_via(self):

        designSettings = self.board_manager.board.GetDesignSettings()
        minTraceWidth = (
            designSettings.m_TrackMinWidth
            if designSettings.m_TrackMinWidth != 0
            else None
        )
        minTraceClearance = designSettings.m_MinClearance
        minHoleSize = (
            designSettings.m_MinThroughDrill
            if designSettings.m_MinThroughDrill != 0
            else None
        )

        tracks: "list[PCB_TRACK]" = self.board_manager.board.Tracks()
        for i in tracks:
            type_id = i.Type()
            if type_id in (PCB_TRACE_T, PCB_ARC_T):
                if minTraceWidth is None:
                    minTraceWidth = i.GetWidth()
                    continue
                minTraceWidth = min(minTraceWidth, i.GetWidth())
            elif type_id == PCB_VIA_T:
                if minHoleSize is None:
                    minHoleSize = i.GetDrillValue()
                    continue
                minHoleSize = min(minHoleSize, i.GetDrillValue())

        self.set_min_trace(
            pcbnew.ToMils(minTraceWidth), pcbnew.ToMils(minTraceClearance)
        )
        self.set_min_hole(pcbnew.ToMM(minHoleSize))
