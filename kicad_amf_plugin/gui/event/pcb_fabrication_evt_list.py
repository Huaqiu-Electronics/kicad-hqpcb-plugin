import wx.lib.newevent as ne

LocaleChangeEvent, EVT_LOCALE_CHANGE = ne.NewCommandEvent()

PackageChangeEvt, EVT_PACKAGE_CHANGE = ne.NewCommandEvent()

MarginModeChangedEvt, EVT_MARGIN_MODE_CHANGE = ne.NewCommandEvent()

SurfaceProcessChanged, EVT_SURFACE_PROCESS_CHANGE = ne.NewCommandEvent()

HDIChanged, EVT_HDI_CHANGE = ne.NewCommandEvent()

ReportChanged, EVT_REPORT_CHANGE = ne.NewCommandEvent()

UpdatePrice, EVT_UPDATE_PRICE = ne.NewCommandEvent()

PlaceOrder, EVT_PLACE_ORDER = ne.NewCommandEvent()

MaskColorChange, EVT_MASK_COLOR_CHANGE = ne.NewCommandEvent()

LayerCountChange, EVT_LAYER_COUNT_CHANGE = ne.NewCommandEvent()

OrderRegionChanged, EVT_ORDER_REGION_CHANGED = ne.NewCommandEvent()
