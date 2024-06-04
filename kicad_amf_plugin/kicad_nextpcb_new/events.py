from wx.lib.newevent import NewEvent

ResetGaugeEvent, EVT_RESET_GAUGE_EVENT = NewEvent()
UpdateGaugeEvent, EVT_UPDATE_GAUGE_EVENT = NewEvent()
MessageEvent, EVT_MESSAGE_EVENT = NewEvent()
AssignPartsEvent, EVT_ASSIGN_PARTS_EVENT = NewEvent()
UpdateSetting, EVT_UPDATE_SETTING = NewEvent()


# part selector
ExportCSV, EVT_EXPORT_CSV = NewEvent()

CacheBitmapInDatabase, EVT_CACHE_BITMAP_IN_DATABASE = NewEvent()

