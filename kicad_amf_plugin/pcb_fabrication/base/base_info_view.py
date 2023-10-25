from kicad_amf_plugin.kicad.board_manager import BoardManager
from kicad_amf_plugin.order.supported_region import SupportedRegion
from kicad_amf_plugin.settings.setting_manager import SETTING_MANAGER
from kicad_amf_plugin.settings.single_plugin import SINGLE_PLUGIN
from kicad_amf_plugin.utils.form_panel_base import FormKind, FormPanelBase
from .base_info_model import BaseInfoModel
from kicad_amf_plugin.gui.event.pcb_fabrication_evt_list import LayerCountChange
from .ui_base_info import (
    UiBaseInfo,
    BOX_SIZE_SETTING,
    BOX_PANEL_SETTING,
    BOX_BREAK_AWAY,
)
from kicad_amf_plugin.utils.validators import (
    NumericTextCtrlValidator,
    FloatTextCtrlValidator,
)
from kicad_amf_plugin.utils.roles import EditDisplayRole
from kicad_amf_plugin.settings.form_value_fitter import fitter_and_map_form_value
from kicad_amf_plugin.settings.supported_layer_count import AVAILABLE_LAYER_COUNTS

import pcbnew
import wx


AVAILABLE_MATERIAL_TYPES = ["FR-4"]

AVAILABLE_BOARD_TG_TYPES = ["TG130", "TG150", "TG170"]


class PcbPackageKind:
    SINGLE_PIECE = 1
    PANEL_BY_CUSTOMER = 3
    PANEL_BY_NEXT_PCB = 2

    PCB_PACKAGE_KIND = (
        EditDisplayRole(SINGLE_PIECE, _("Single Piece")),
        EditDisplayRole(PANEL_BY_CUSTOMER, _("Panel by Customer")),
        EditDisplayRole(PANEL_BY_NEXT_PCB, _("Panel by NextPCB")),
    )


class MarginMode:
    NA = "N/A"
    LEFT_RIGHT = "X"
    TOP_BOTTOM = "Y"
    ALL_4_SIDE = "XY"

    MARGIN_MODE_CHOICE = [
        EditDisplayRole(NA, _("N/A")),
        EditDisplayRole(LEFT_RIGHT, _("Left & Right")),
        EditDisplayRole(TOP_BOTTOM, _("Top & Bottom")),
        EditDisplayRole(ALL_4_SIDE, _("All 4 sides")),
    ]


AVAILABLE_QUANTITY = [
    5,
    10,
    15,
    20,
    25,
    30,
    40,
    50,
    75,
    100,
    125,
    150,
    200,
    250,
    300,
    350,
    400,
    450,
    500,
    600,
    700,
    800,
    900,
    1000,
    1500,
    2000,
    2500,
    3000,
    3500,
    4000,
    4500,
    5000,
    5500,
    6000,
    6500,
    7000,
    7500,
    8000,
    9000,
    10000,
]


class BaseInfoView(UiBaseInfo, FormPanelBase):
    def __init__(self, parent, board_manager: BoardManager):
        super().__init__(parent)
        self.board_manager = board_manager

        self.combo_pcb_package_kind.Bind(wx.EVT_CHOICE, self.on_pcb_packaging_changed)
        self.comb_margin_mode.Bind(wx.EVT_CHOICE, self.on_margin_mode_changed)
        self.combo_layer_count.Bind(wx.EVT_CHOICE, self.on_layer_count_changed)
        for editor in self.edit_panel_x, self.edit_panel_y:
            editor.SetValidator(NumericTextCtrlValidator())
        self.edit_margin_size.SetValidator(FloatTextCtrlValidator())

    def is_valid(self) -> bool:
        if (
            self.pcb_package_kind != PcbPackageKind.SINGLE_PIECE
            and not self.should_apply_single_board_geometry()
        ):
            if not self.edit_panel_x.Validate():
                wx.MessageBox(
                    _("Panel Type X value isn't valid. Please input valid value."),
                    _("Error"),
                    wx.OK | wx.ICON_ERROR,
                )
                return False
            if not self.edit_panel_y.Validate():
                wx.MessageBox(
                    _("Panel Type Y value isn't valid. Please input valid value."),
                    _("Error"),
                    wx.OK | wx.ICON_ERROR,
                )
                return False
        if self.edit_margin_size.Enabled:
            if not self.edit_margin_size.Validate():
                wx.MessageBox(
                    _("Break-away Rail value isn't valid. Please input valid value."),
                    _("Error"),
                    wx.OK | wx.ICON_ERROR,
                )
                return False
        return True

    @property
    def box_piece_or_panel_size(self):
        return self.FindWindowById(BOX_SIZE_SETTING)

    @property
    def box_panel_setting(self):
        return self.FindWindowById(BOX_PANEL_SETTING)

    @property
    def box_break_away(self):
        return self.FindWindowById(BOX_BREAK_AWAY)

    @property
    def pcb_package_kind(self):
        return PcbPackageKind.PCB_PACKAGE_KIND[
            int(self.combo_pcb_package_kind.GetSelection())
        ].EditRole

    @property
    def margin_mode(self):
        return MarginMode.MARGIN_MODE_CHOICE[
            int(self.comb_margin_mode.GetSelection())
        ].EditRole

    def should_apply_single_board_geometry(self):
        return (
            self.pcb_package_kind == PcbPackageKind.SINGLE_PIECE
            or SETTING_MANAGER.order_region == SupportedRegion.CHINA_MAINLAND
            and self.pcb_package_kind
            in (PcbPackageKind.SINGLE_PIECE, PcbPackageKind.PANEL_BY_CUSTOMER)
        )

    def get_pcb_length(self):
        """Default is mm


        Returns:
            _type_: float
        """
        if self.should_apply_single_board_geometry():
            if self.margin_mode in (MarginMode.LEFT_RIGHT, MarginMode.ALL_4_SIDE):
                return (
                    float(self.edit_size_x.GetValue())
                    + float(self.edit_margin_size.GetValue()) * 2
                )
            else:
                return float(self.edit_size_x.GetValue())
        else:
            if self.margin_mode in (MarginMode.LEFT_RIGHT, MarginMode.ALL_4_SIDE):
                return (
                    float(self.edit_size_x.GetValue())
                    * int(self.edit_panel_x.GetValue())
                    + float(self.edit_margin_size.GetValue()) * 2
                )
            else:
                return float(self.edit_size_x.GetValue()) * int(
                    self.edit_panel_x.GetValue()
                )

    def get_pcb_width(self):
        """Default is mm


        Returns:
            _type_: float
        """
        if self.should_apply_single_board_geometry():
            if self.margin_mode in (MarginMode.LEFT_RIGHT, MarginMode.ALL_4_SIDE):
                return (
                    float(self.edit_size_y.GetValue())
                    + float(self.edit_margin_size.GetValue()) * 2
                )
            else:
                return float(self.edit_size_y.GetValue())
        else:
            if self.margin_mode in (MarginMode.LEFT_RIGHT, MarginMode.ALL_4_SIDE):
                return (
                    float(self.edit_size_y.GetValue())
                    * int(self.edit_panel_y.GetValue())
                    + float(self.edit_margin_size.GetValue()) * 2
                )
            else:
                return float(self.edit_size_y.GetValue()) * int(
                    self.edit_panel_y.GetValue()
                )

    @fitter_and_map_form_value
    def get_from(self, kind: FormKind) -> "dict":
        data = BaseInfoModel(
            blayer=self.combo_layer_count.GetStringSelection(),
            plate_type=AVAILABLE_MATERIAL_TYPES[0],
            board_tg=self.combo_board_tg.GetStringSelection()
            if self.combo_board_tg.Enabled
            else None,
            units=str(self.pcb_package_kind),
            blength=str(
                FormPanelBase.convert_geometry(
                    kind, SETTING_MANAGER.order_region, self.get_pcb_length()
                )
            ),
            bwidth=str(
                FormPanelBase.convert_geometry(
                    kind, SETTING_MANAGER.order_region, self.get_pcb_width()
                )
            ),
            bcount=self.combo_quantity.GetStringSelection(),
            sidedirection=str(self.margin_mode),
        )

        if self.pcb_package_kind in (
            PcbPackageKind.PANEL_BY_CUSTOMER,
            PcbPackageKind.PANEL_BY_NEXT_PCB,
        ):
            if not self.order_region_is_cn_and_package_by_customer():
                data.layoutx = self.edit_panel_x.GetValue()
                data.layouty = self.edit_panel_y.GetValue()

        if self.margin_mode != MarginMode.NA:
            data.sidewidth = self.edit_margin_size.GetValue()

        return vars(data)

    def order_region_is_cn_and_package_by_customer(self):
        return (
            SETTING_MANAGER.order_region == SupportedRegion.CHINA_MAINLAND
            and self.pcb_package_kind == PcbPackageKind.PANEL_BY_CUSTOMER
        )

    def init(self):
        self.initUI()
        self.loadBoardInfo()

    def getBaseInfo(self):
        return self.base_info

    def initUI(self):
        self.combo_material_type.Append(AVAILABLE_MATERIAL_TYPES)
        self.combo_material_type.SetSelection(0)

        self.combo_layer_count.AppendItems([str(i) for i in AVAILABLE_LAYER_COUNTS])
        self.combo_layer_count.SetSelection(1)

        self.combo_pcb_package_kind.Append(
            [i.DisplayRole for i in PcbPackageKind.PCB_PACKAGE_KIND]
        )
        self.comb_margin_mode.Append(
            [i.DisplayRole for i in MarginMode.MARGIN_MODE_CHOICE]
        )

        self.combo_quantity.Append([str(i) for i in AVAILABLE_QUANTITY])
        self.combo_quantity.SetSelection(0)
        self.comb_margin_mode.SetSelection(0)
        self.combo_pcb_package_kind.SetSelection(0)

        self.combo_board_tg.Append(AVAILABLE_BOARD_TG_TYPES)
        self.combo_board_tg.SetSelection(0)

        for i in self.edit_size_x, self.edit_size_y:
            i.SetEditable(False)
        self.edit_margin_size.Enabled = False
        self.box_panel_setting.Show(
            self.pcb_package_kind != PcbPackageKind.SINGLE_PIECE
        )

    def loadBoardInfo(self):
        boardWidth = pcbnew.ToMM(
            self.board_manager.board.GetBoardEdgesBoundingBox().GetWidth()
        )
        boardHeight = pcbnew.ToMM(
            self.board_manager.board.GetBoardEdgesBoundingBox().GetHeight()
        )
        layerCount = self.board_manager.board.GetCopperLayerCount()
        self.combo_layer_count.SetSelection(
            self.combo_layer_count.FindString(str(layerCount))
        )
        self.combo_layer_count.Enabled = False
        self.edit_size_x.SetValue(str(boardWidth))
        self.edit_size_y.SetValue(str(boardHeight))
        self.combo_board_tg.Enabled = layerCount > 3

    def on_pcb_packaging_changed(self, evt=None):
        if self.pcb_package_kind == PcbPackageKind.SINGLE_PIECE:
            self.box_piece_or_panel_size.SetLabelText(_("Size (single)"))
            self.label_quantity.SetLabel(_("Qty(single)"))
            self.label_quantity_unit.SetLabel(_("Pcs"))
        else:
            self.box_piece_or_panel_size.SetLabelText(_("Size (set)"))
            self.label_quantity.SetLabel(_("Qty(Set)"))
            self.label_quantity_unit.SetLabel(_("Set"))

        self.box_panel_setting.Show(
            self.pcb_package_kind != PcbPackageKind.SINGLE_PIECE
            and not self.order_region_is_cn_and_package_by_customer()
        )
        self.box_break_away.Enabled = (
            self.pcb_package_kind != PcbPackageKind.PANEL_BY_CUSTOMER
        )
        self.on_margin_mode_changed()
        if SINGLE_PLUGIN.get_main_wind() is not None:
            SINGLE_PLUGIN.get_main_wind().adjust_size()

    def on_margin_mode_changed(self, event=None):
        self.edit_margin_size.Enabled = self.margin_mode != MarginMode.NA
        if self.margin_mode == MarginMode.NA:
            self.edit_margin_size.SetValue("0")

    def on_layer_count_changed(self, evt):
        evt = LayerCountChange(id=-1)
        count = int(self.combo_layer_count.GetStringSelection())
        evt.SetInt(count)
        self.combo_board_tg.Enabled = count > 3
        wx.PostEvent(self.Parent, evt)

    def get_pcb_count(self):
        n = int(self.combo_quantity.GetStringSelection())
        if (
            self.combo_pcb_package_kind.GetSelection() == 1
            or self.combo_pcb_package_kind.GetSelection() == 2
        ):
            return (
                n
                * int(self.edit_panel_x.GetValue())
                * int(self.edit_panel_y.GetValue())
            )
        else:
            return n

    def on_region_changed(self):
        self.on_pcb_packaging_changed(None)
