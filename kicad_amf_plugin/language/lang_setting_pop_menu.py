import wx
from .lang_const import CODE_TO_NAME, code_to_wx
from kicad_amf_plugin.settings.setting_manager import SETTING_MANAGER


WX_ID_MAP = code_to_wx()


class LangSettingPopMenu(wx.Menu):
    def __init__(self, current_lang_id: int):
        super().__init__()
        for lang in enumerate(CODE_TO_NAME):
            id, code = lang
            item = wx.MenuItem(id=id, text=_(CODE_TO_NAME[code]), kind=wx.ITEM_CHECK)
            wx_id = WX_ID_MAP[code]
            if current_lang_id == wx_id:
                item.Check(True)
            else:
                item.Check(False)
            self.Append(item)
            if wx.LANGUAGE_ENGLISH == wx_id:
                self.Bind(wx.EVT_MENU, self.setup_en, id=id)
            elif wx.LANGUAGE_JAPANESE_JAPAN == wx_id:
                self.Bind(wx.EVT_MENU, self.setup_jp, id=id)
            elif wx.LANGUAGE_CHINESE_SIMPLIFIED == wx_id:
                self.Bind(wx.EVT_MENU, self.setup_zh, id=id)

    def setup_en(self, evt):
        SETTING_MANAGER.set_language(wx.LANGUAGE_ENGLISH)

    def setup_jp(self, evt):
        SETTING_MANAGER.set_language(wx.LANGUAGE_JAPANESE_JAPAN)

    def setup_zh(self, evt):
        SETTING_MANAGER.set_language(wx.LANGUAGE_CHINESE_SIMPLIFIED)
