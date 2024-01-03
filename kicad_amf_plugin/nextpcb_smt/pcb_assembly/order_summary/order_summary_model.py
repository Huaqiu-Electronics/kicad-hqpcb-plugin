from dataclasses import dataclass
import wx.dataview as dv
from kicad_amf_plugin.gui.summary.price_model_base import PriceModelCol, PriceModelBase, PriceItem
from kicad_amf_plugin.gui.summary.pcb_price_model import PCBPriceModel
from .pcba_price_model import PCBAPriceModel

from enum import Enum
from kicad_amf_plugin.settings.setting_manager import SETTING_MANAGER


class PriceCategory(Enum):
    PCB = "pcb"
    PCBA = "PCBA"
    
PRICE_KIND = 2    
    
class OrderSummaryModel(dv.PyDataViewModel):
    def __init__(self):
        dv.PyDataViewModel.__init__(self)
        self.UseWeakRefs(True)
        self.price_category: "dict[int,PriceModelBase]" = {
            PriceCategory.PCB: PCBPriceModel(),
            PriceCategory.PCBA: PCBAPriceModel(),
        }

        self._days_cost = 0
        self._pcb_quantity = 0
    
    
    def GetColumnCount(self):
        return PriceModelCol.COL_COUNT

    def GetColumnType(self, col):
        mapper = {
            0: "string",
            1: "string",
        }
        return mapper[col]

    def GetChildren(self, parent, children):
        if not parent:
            for cat in self.price_category:
                children.append(self.ObjectToItem(self.price_category[cat]))
            return PRICE_KIND

        # Otherwise we'll fetch the python object associated with the parent
        # item and make DV items for each of its child objects.
        node = self.ItemToObject(parent)
        if isinstance(node, PriceModelBase):
            for i in node.get_items():
                children.append(self.ObjectToItem(i))
            return len(node.get_items())
        return 0    
      
    def IsContainer(self, item):
        # Return True if the item has children, False otherwise.
        ##self.log.write("IsContainer\n")

        # The hidden root is a container
        if not item:
            return True
        # and in this model the genre objects are containers
        node = self.ItemToObject(item)
        if isinstance(node, PriceModelBase):
            return True
        # but everything else (the song objects) are not
        return False
      
    def GetParent(self, item):
        # Return the item which is this item's parent.
        ##self.log.write("GetParent\n")

        if not item:
            return dv.NullDataViewItem

        node = self.ItemToObject(item)
        if isinstance(node, PriceModelBase):
            return dv.NullDataViewItem
        elif isinstance(node, PriceItem):
            return self.ObjectToItem(node.parent)
        return dv.NullDataViewItem

    def HasValue(self, item, col):
        # Overriding this method allows you to let the view know if there is any
        # data at all in the cell. If it returns False then GetValue will not be
        # called for this item and column.
        node = self.ItemToObject(item)
        if isinstance(node, PriceModelBase) or isinstance(node, PriceItem):
            return True
        return False

    def GetValue(self, item, col):
        # Return the value to be displayed for this item and column. For this
        # example we'll just pull the values from the data objects we
        # associated with the items in GetChildren.

        # Fetch the data object for this item.
        node = self.ItemToObject(item)

        if isinstance(node, PriceModelBase):
            # Due to the HasValue implementation above, GetValue should only
            # be called for the first column for PriceModelBase objects. We'll verify
            # that with this assert.
            if 0 == col:
                return node.name()
            else:
                return f"{node.sum()}{SETTING_MANAGER.get_price_unit()}"

        elif isinstance(node, PriceItem):
            mapper = {
                0: node.desc,
                1: f"{node.value}{SETTING_MANAGER.get_price_unit()}",
            }
            return mapper[col]

        else:
            raise RuntimeError("unknown node type")

    def GetAttr(self, item, col, attr):
        node = self.ItemToObject(item)
        if (
            isinstance(node, PCBPriceModel)
            or isinstance(node, PCBAPriceModel)
        ):
            attr.SetColour("blue")
            attr.SetBold(True)
            return True
        return False

    def clear_content(self):
        for i in PriceCategory.PCB, PriceCategory.SMT, PriceCategory.BOM:
            self.price_category[i].clear()
        self.Cleared()