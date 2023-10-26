import wx
import os
from kicad_amf_plugin.gui.event.pcb_fabrication_evt_list import LocaleChangeEvent
from .kicad_setting import KiCadSetting
from kicad_amf_plugin.order.supported_region import SupportedRegion
from kicad_amf_plugin.utils.public_ip import get_ip_country

APP_NAME = "kicad_amf_plugin"

VENDOR_NAME = "NextPCB"

LANGUAGE = "language"

ORDER_REGION = "order_region"

WIDTH = "width"

HEIGHT = "height"

PRICE_UNIT = {0: "¥", 1: "$"}

TRANSLATED_PRICE_UNIT = {"¥": "元", "$": "美元"}


CN_JP_BUILD_TIME_FORMATTER = "{time}{unit}"

EN_BUILD_TIME_FORMATTER = "{time} {unit}"


class _SettingManager(wx.EvtHandler):
    def __init__(self) -> None:
        self.app: wx.App = None
        sp = wx.StandardPaths.Get()
        config_loc = sp.GetUserConfigDir()
        config_loc = os.path.join(config_loc, APP_NAME)

        if not os.path.exists(config_loc):
            os.mkdir(config_loc)

        self.app_conf = wx.FileConfig(
            appName=APP_NAME,
            vendorName=VENDOR_NAME,
            localFilename=os.path.join(config_loc, "common.ini"),
        )

        if not self.app_conf.HasEntry(LANGUAGE):
            self.set_language(KiCadSetting.read_lang_setting())
            self.app_conf.Flush()
        if not self.app_conf.HasEntry(WIDTH) or not self.app_conf.HasEntry(HEIGHT):
            self.set_window_size((660, 700))
        if not self.app_conf.HasEntry(ORDER_REGION):
            location = "China"
            try:
                location = get_ip_country()
            except:
                pass
            if location == "China":
                self.set_order_region(SupportedRegion.CHINA_MAINLAND)
            elif location == "Japan":
                self.set_order_region(SupportedRegion.JAPAN)
            else:
                self.set_order_region(SupportedRegion.EUROPE_USA)

    def register_app(self, app: wx.App):
        self.app = app

    def set_language(self, now: int):
        old = self.language
        if old == now:
            return
        self.app_conf.WriteInt(key=LANGUAGE, value=now)
        if self.app:
            evt = LocaleChangeEvent(id=-1)
            evt.SetInt(now)
            self.app_conf.Flush()
            wx.PostEvent(self.app, evt)

    @property
    def language(self):
        return self.app_conf.ReadInt(LANGUAGE)

    def set_order_region(self, region: int):
        self.app_conf.WriteInt(key=ORDER_REGION, value=region)

    @property
    def order_region(self):
        return self.app_conf.ReadInt(ORDER_REGION)

    def get_price_unit(self, translated=False):
        sym = "¥" if not self.order_region else "$"
        if not translated:
            return sym
        if self.language == wx.LANGUAGE_CHINESE_SIMPLIFIED:
            return TRANSLATED_PRICE_UNIT[sym]
        return sym

    def get_build_time_formatter(self):
        return (
            EN_BUILD_TIME_FORMATTER
            if SupportedRegion.EUROPE_USA == self.order_region
            else CN_JP_BUILD_TIME_FORMATTER
        )

    def set_window_size(self, s: "tuple[int,int]"):
        self.app_conf.WriteInt(key=WIDTH, value=s[0])
        self.app_conf.WriteInt(key=HEIGHT, value=s[1])
        self.app_conf.Flush()

    def get_window_size(self):
        return wx.Size(self.app_conf.ReadInt(WIDTH), self.app_conf.ReadInt(HEIGHT))


SETTING_MANAGER = _SettingManager()
