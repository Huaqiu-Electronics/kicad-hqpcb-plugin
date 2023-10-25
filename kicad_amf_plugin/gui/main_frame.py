from kicad_amf_plugin.gui.summary.price_summary_model import PriceCategory
from kicad_amf_plugin.kicad.board_manager import BoardManager
from kicad_amf_plugin.order.supported_region import SupportedRegion
from kicad_amf_plugin.pcb_fabrication.base.base_info_view import BaseInfoView
from kicad_amf_plugin.pcb_fabrication.process.process_info_view import ProcessInfoView
from kicad_amf_plugin.pcb_fabrication.special_process.special_process_view import (
    SpecialProcessView,
)
from kicad_amf_plugin.pcb_fabrication.personalized.personalized_info_view import (
    PersonalizedInfoView,
)
from kicad_amf_plugin.gui.summary.summary_panel import SummaryPanel
from kicad_amf_plugin.settings.default_express import DEFAULT_EXPRESS
from kicad_amf_plugin.settings.single_plugin import SINGLE_PLUGIN
from kicad_amf_plugin.utils.form_panel_base import FormKind, FormPanelBase
from kicad_amf_plugin.gui.event.pcb_fabrication_evt_list import (
    EVT_LAYER_COUNT_CHANGE,
    EVT_UPDATE_PRICE,
    EVT_PLACE_ORDER,
    EVT_ORDER_REGION_CHANGED,
)
from kicad_amf_plugin.settings.setting_manager import SETTING_MANAGER
from kicad_amf_plugin.kicad.fabrication_data_generator import FabricationDataGenerator
from kicad_amf_plugin.api.base_request import BaseRequest
from kicad_amf_plugin.utils.request_helper import RequestHelper
from kicad_amf_plugin.gui.summary.order_summary_model import (
    AVAILABLE_TIME_UNIT,
    OrderSummary,
    BuildTime,
    TimeUnit,
)
import wx
import wx.xrc
import wx.dataview
import urllib
import requests
import webbrowser
import json
from kicad_amf_plugin.order.order_region import OrderRegion, URL_KIND
from enum import Enum


class PCBFormPart(Enum):
    BASE_INFO = 0
    PROCESS_INFO = 1
    SPECIAL_PROCESS = 2
    PERSONALIZED = 3


PCB_PANEL_CTORS = {
    PCBFormPart.BASE_INFO: BaseInfoView,
    PCBFormPart.PROCESS_INFO: ProcessInfoView,
    PCBFormPart.SPECIAL_PROCESS: SpecialProcessView,
    PCBFormPart.PERSONALIZED: PersonalizedInfoView,
}

DATA = "data"
LIST = "list"
SUGGEST = "suggest"
DEL_TIME = "deltime"
NAME = "name"
PCS_COUNT = "pcs_count"
TOTAL = "total"
PCB = "pcb"
FEE = "fee"
BCOUNT = "bcount"


class MainFrame(wx.Frame):
    def __init__(self, board_manager: BoardManager, size, parent=None):
        wx.Frame.__init__(
            self,
            parent,
            id=wx.ID_ANY,
            title=_("HQ NextPCB Active Manufacturing"),
            pos=wx.DefaultPosition,
            size=size,
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
        )
        self._board_manager = board_manager
        self._fabrication_data_gen = None
        self._pcb_form_parts: "dict[PCBFormPart, FormPanelBase]" = {}
        SINGLE_PLUGIN.register_main_wind(self)
        self.init_ui()

    def init_ui(self):
        wx.SizerFlags.DisableConsistencyChecks()
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        pcb_fab_scroll_wind = wx.ScrolledWindow(
            self,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.Size(-1, -1),
            wx.HSCROLL | wx.VSCROLL,
        )
        pcb_fab_scroll_wind.SetScrollRate(10, 10)

        lay_pcb_fab_panel = wx.BoxSizer(wx.VERTICAL)
        for i in PCB_PANEL_CTORS:
            view = PCB_PANEL_CTORS[i](pcb_fab_scroll_wind, self._board_manager)
            self._pcb_form_parts[i] = view
            lay_pcb_fab_panel.Add(view, 0, wx.ALL | wx.EXPAND, 5)
        pcb_fab_scroll_wind.SetSizer(lay_pcb_fab_panel)
        pcb_fab_scroll_wind.Layout()

        self.summary_view = SummaryPanel(self)
        main_sizer.Add(pcb_fab_scroll_wind, 1, wx.EXPAND, 8)
        main_sizer.Add(self.summary_view, 0, wx.EXPAND, 8)

        self.Bind(
            EVT_LAYER_COUNT_CHANGE,
            self._pcb_form_parts[PCBFormPart.PROCESS_INFO].setup_board_thickness_choice,
        )
        self.Bind(
            EVT_LAYER_COUNT_CHANGE,
            self._pcb_form_parts[PCBFormPart.SPECIAL_PROCESS].on_layer_count_changed,
        )
        self.Bind(EVT_UPDATE_PRICE, self.on_update_price)
        self.Bind(EVT_PLACE_ORDER, self.on_place_order)
        self.Bind(EVT_ORDER_REGION_CHANGED, self.on_order_region_changed)
        self.Bind(wx.EVT_SIZE, self.OnSize, self)
        self.Bind(wx.EVT_CLOSE, self.OnClose, self)

        for i in self._pcb_form_parts.values():
            i.init()
            i.on_region_changed()

        self.SetSizer(main_sizer)
        self.Layout()
        self.Centre(wx.BOTH)

    @property
    def fabrication_data_generator(self):
        if self._fabrication_data_gen is None:
            self._fabrication_data_gen = FabricationDataGenerator(
                self._board_manager.board
            )
        return self._fabrication_data_gen

    def build_form(self, kind: FormKind):
        base = BaseRequest().__dict__
        for i in self._pcb_form_parts.values():
            base = base | i.get_from(kind)
        return base

    def get_query_price_form(self):
        form = self.build_form(FormKind.QUERY_PRICE)
        if SETTING_MANAGER.order_region == SupportedRegion.CHINA_MAINLAND:
            form = form | DEFAULT_EXPRESS
        return form

    def get_place_order_form(self):
        return {**self.build_form(FormKind.PLACE_ORDER), "type": "pcbfile"}

    def form_is_valid(self):
        for i in self._pcb_form_parts.values():
            if not i.is_valid():
                return False
        return True

    def parse_zh_data_time(self, dt: str):
        t = ""
        unit = None
        for i in dt:
            if i.isnumeric():
                t = t + i
            elif "天" == i:
                unit = TimeUnit.DAY.value
        if unit is None:
            unit = TimeUnit.HOUR.value
        return BuildTime(int(t), unit)

    def parse_price(self, summary: json):
        self.summary_view.update_price_detail({PriceCategory.PCB.value: summary})
        normal_total_price = self.summary_view.get_total_price()
        suggests = []
        if SUGGEST in summary and DEL_TIME in summary[SUGGEST]:
            for suggest in summary[SUGGEST][DEL_TIME]:
                if NAME in suggest and FEE in suggest and BCOUNT in suggest:
                    qty = int(suggest[BCOUNT])
                    price = float(suggest[FEE]) + normal_total_price
                    suggests.append(
                        OrderSummary(
                            pcb_quantity=qty,
                            price=price,
                            build_time=self.parse_zh_data_time(suggest[NAME]),
                        )
                    )
        self.summary_view.update_order_summary(suggests)

    def parse_price_list(self, summary: json):
        self.summary_view.update_price_detail(summary)
        suggests = []
        for item in summary:
            if SUGGEST in summary[item] and DEL_TIME in summary[item][SUGGEST]:
                for suggest in summary[item][SUGGEST][DEL_TIME]:
                    if NAME in suggest and TOTAL in suggest and PCS_COUNT in suggest:
                        full_time_cost = str(suggest[NAME]).split(" ")
                        if len(full_time_cost) > 1:
                            qty = int(suggest[PCS_COUNT])
                            price = float(suggest[TOTAL])
                            suggests.append(
                                OrderSummary(
                                    pcb_quantity=qty,
                                    price=price,
                                    build_time=BuildTime(
                                        int(full_time_cost[0]), full_time_cost[1]
                                    ),
                                )
                            )
        self.summary_view.update_order_summary(suggests)

    def on_update_price(self, evt):
        if not self.form_is_valid():
            return
        url = OrderRegion.get_url(SETTING_MANAGER.order_region, URL_KIND.QUERY_PRICE)
        if url is None:
            wx.MessageBox(_("No available url for querying price in current region"))
            return
        try:
            form = self.get_query_price_form()
            rep = urllib.request.Request(
                url, data=RequestHelper.convert_dict_to_request_data(form)
            )
            fp = urllib.request.urlopen(rep)
            data = fp.read()
            encoding = fp.info().get_content_charset("utf-8")
            content = data.decode(encoding)
            quote = json.loads(content)
            if DATA in quote and LIST in quote[DATA]:
                return self.parse_price_list(quote[DATA][LIST])
            elif SUGGEST in quote:
                return self.parse_price(quote)
            else:
                err_msg = quote
                if "msg" in quote:
                    err_msg = quote["msg"]
                wx.MessageBox(_("Incorrect form parameter: ") + err_msg)
        except Exception as e:
            wx.MessageBox(str(e))
            raise e  # TODO remove me

    def on_place_order(self, evt):
        if not self.form_is_valid():
            return
        try:
            url = OrderRegion.get_url(
                SETTING_MANAGER.order_region, URL_KIND.PLACE_ORDER
            )
            if url is None:
                wx.MessageBox(_("No available url for placing order in current region"))
                return
            with self.fabrication_data_generator.create_kicad_pcb_file() as zipfile:
                rsp = requests.post(
                    url,
                    files={"file": open(zipfile, "rb")},
                    data=self.get_place_order_form(),
                )
                urls = json.loads(rsp.content)
                for key in "url", "redirect":
                    if key in urls:
                        uat_url = str(urls[key])
                        webbrowser.open(uat_url)
                        return
                raise Exception("No available order url in the response")
        except Exception as e:
            wx.MessageBox(str(e))
            raise e  # TODO remove me

    def adjust_size(self):
        for i in self._pcb_form_parts.values():
            i.Layout()
        self.Layout()

    def on_order_region_changed(self, ev):
        for i in self._pcb_form_parts.values():
            i.on_region_changed()
        self.adjust_size()

    def OnSize(self, evt):
        evt.Skip()
        SETTING_MANAGER.set_window_size(self.Size)

    def OnClose(self, evt):
        SINGLE_PLUGIN.register_main_wind(None)
        self.Destroy()
