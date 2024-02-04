import wx
import sys
from wx.lib.mixins.inspection import InspectionMixin
from kicad_amf_plugin.kicad_nextpcb_new.mainwindow import NextPCBTools


def _main():
    app = BaseApp()
    app.MainLoop()


def _displayHook(obj):
    if obj is not None:
        print(repr(obj))


class BaseApp(wx.App, InspectionMixin):
    def __init__(self):
        super().__init__()
        self.Init()
        sys.displayhook = _displayHook
        self.locale = None
        self.startup_dialog()
        return None

    def startup_dialog(self):
        self.w = NextPCBTools(None)
        self.w.Show()
