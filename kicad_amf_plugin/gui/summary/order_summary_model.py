from dataclasses import dataclass
import wx.dataview as dv
from kicad_amf_plugin.settings.setting_manager import SETTING_MANAGER
from enum import Enum

from collections import namedtuple


class TimeUnit(Enum):
    DAY = "days"
    HOUR = "hours"


AVAILABLE_TIME_UNIT = {TimeUnit.DAY.value: _("days"), TimeUnit.HOUR.value: _("hours")}

BuildTime = namedtuple("BuildTime", ["Time", "Unit"])


class OrderSummaryCol:
    BUILD_TIME = 0
    QUANTITY = BUILD_TIME + 1
    PRICE = QUANTITY + 1

    COL_COUNT = PRICE + 1


@dataclass
class OrderSummary:
    pcb_quantity: int
    build_time: BuildTime
    price: float


class OrderSummaryModel(dv.DataViewIndexListModel):
    def __init__(self):
        dv.DataViewIndexListModel.__init__(self)
        self.orders_summary: "list[OrderSummary]" = []

    # This method is called to provide the data object for a
    # particular row,col
    def GetValueByRow(self, row: int, col: int):
        order = self.orders_summary[row]
        map = {
            0: SETTING_MANAGER.get_build_time_formatter().format(
                time=order.build_time.Time, unit=_(order.build_time.Unit)
            ),
            1: str(order.pcb_quantity),
            2: f"{SETTING_MANAGER.get_price_unit()}{order.price}",
        }
        return map[col]

    # Report how many columns this model provides data for.
    def GetColumnCount(self):
        return OrderSummaryCol.COL_COUNT

    # Specify the data type for a column
    def GetColumnType(self, col):
        return "string"

    def SetValueByRow(self, value, row, col):
        return False

    # Report the number of rows in the model
    def GetCount(self):
        # self.log.write('GetCount')
        return len(self.orders_summary)

    # Called to check if non-standard attributes should be used in the
    # cell at (row, col)
    def GetAttrByRow(self, row, col, attr):
        # self.log.write('GetAttrByRow: (%d, %d)' % (row, col))
        # if col == 3:
        #     attr.SetColour('red')
        #     attr.SetBold(True)
        #     return True
        return False

    def update_order_info(self, data: "list[OrderSummary]"):
        self.orders_summary = data
        self.Reset(len(data))

    def clear_content(self):
        self.orders_summary = []
        self.Reset(len(self.orders_summary))
        self.Cleared()
