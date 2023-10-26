from wx.lib.mixins.inspection import InspectionMixin
from kicad_amf_plugin.language.lang_const import get_supported_language
from kicad_amf_plugin.language.lang_const import LANG_DOMAIN
from kicad_amf_plugin.settings.supported_layer_count import AVAILABLE_LAYER_COUNTS
import builtins
import sys
import os
from kicad_amf_plugin import PLUGIN_ROOT
from kicad_amf_plugin.gui.event.pcb_fabrication_evt_list import EVT_LOCALE_CHANGE
from kicad_amf_plugin.kicad.board_manager import load_board_manager
from kicad_amf_plugin.utils.combo_box_ignore_wheel import ComboBoxIgnoreWheel
import wx

# add translation macro to builtin similar to what gettext does
builtins.__dict__["_"] = wx.GetTranslation
wx.Choice = ComboBoxIgnoreWheel


def _displayHook(obj):
    if obj is not None:
        print(repr(obj))


class BaseApp(wx.App, InspectionMixin):
    def __init__(
        self, redirect=False, filename=None, useBestVisual=False, clearSigInt=True
    ):
        super().__init__(redirect, filename, useBestVisual, clearSigInt)
        self.Bind(EVT_LOCALE_CHANGE, self.on_locale_changed)

    def OnInit(self):
        self.Init()  # InspectionMixin
        # work around for Python stealing "_"
        sys.displayhook = _displayHook
        self.locale = None
        wx.Locale.AddCatalogLookupPathPrefix(
            os.path.join(PLUGIN_ROOT, "language", "locale")
        )
        from kicad_amf_plugin.settings.setting_manager import SETTING_MANAGER

        self.update_language(SETTING_MANAGER.language)
        SETTING_MANAGER.register_app(self)
        self.board_manager = load_board_manager()
        if self.board_manager.board.GetCopperLayerCount() not in AVAILABLE_LAYER_COUNTS:
            wx.MessageBox(_("Unsupported layer count!"))
            return False
        self.startup_dialog()
        return True

    def on_locale_changed(self, evt):
        self.update_language(evt.GetInt())
        info = wx.MessageDialog(
            self.main_wind,
            _(
                "Restart the plugin to apply the new locale ?\nFor full translation(including the options), restarting KiCad is required"
            ),
            _("Tip"),
            wx.YES | wx.ICON_QUESTION | wx.NO,
        )
        res = info.ShowModal()
        info.Destroy()
        if res == wx.ID_YES:
            if self.main_wind:
                self.main_wind.Destroy()
            self.startup_dialog()

    def update_language(self, lang: int):
        if lang in get_supported_language():
            selLang = lang
        else:
            selLang = wx.LANGUAGE_ENGLISH
        if self.locale:
            assert sys.getrefcount(self.locale) <= 2
            del self.locale

        self.locale = wx.Locale(selLang)
        if self.locale.IsOk():
            self.locale.AddCatalog(LANG_DOMAIN)
        else:
            self.locale = None

    def startup_dialog(self):
        from kicad_amf_plugin.gui.main_frame import MainFrame
        from kicad_amf_plugin.settings.setting_manager import SETTING_MANAGER

        self.main_wind = MainFrame(
            self.board_manager, SETTING_MANAGER.get_window_size()
        )
        self.main_wind.Show()
