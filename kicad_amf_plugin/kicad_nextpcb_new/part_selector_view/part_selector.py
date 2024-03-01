import logging

import wx
import requests
import threading
import json
import wx.dataview
from kicad_amf_plugin.kicad_nextpcb_new.events import AssignPartsEvent, UpdateSetting
from kicad_amf_plugin.kicad_nextpcb_new.helpers import HighResWxSize, loadBitmapScaled
from requests.exceptions import Timeout
from .ui_part_details_panel.part_details_view import PartDetailsView
from .ui_search_panel.search_view import SearchView
from .ui_part_list_panel.part_list_view import PartListView

ID_SELECT_PART = wx.NewIdRef()

COLUM_SKU = 5
COLUM_PRICE = 6
COLUM_STOCK = 7


def ceil(x, y):
    return -(-x // y)


class PartSelectorDialog(wx.Dialog):
    def __init__(self, parent, parts):
        wx.SizerFlags.DisableConsistencyChecks()
        wx.Dialog.__init__(
            self,
            parent,
            id=wx.ID_ANY,
            title=_("NextPCB Search Online"),
            pos=wx.DefaultPosition,
            size=HighResWxSize(parent.window, wx.Size(1200, 800)),
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.MAXIMIZE_BOX,
        )

        self.logger = logging.getLogger(__name__)
        self.parent = parent
        self.parts = parts

        self.current_page = 0
        self.total_pages = 0

        part_selection = self.get_existing_selection(parts)
        self.part_info = part_selection.split(",")

        self.part_details_view = PartDetailsView(self)
        self.search_view = SearchView(self)
        self.part_list_view = PartListView(self)
        # ---------------------------------------------------------------------
        # ---------------------------- Hotkeys --------------------------------
        # ---------------------------------------------------------------------
        quitid = wx.NewId()
        self.Bind(wx.EVT_MENU, self.quit_dialog, id=quitid)

        entries = [wx.AcceleratorEntry(), wx.AcceleratorEntry(), wx.AcceleratorEntry()]
        entries[0].Set(wx.ACCEL_CTRL, ord("W"), quitid)
        entries[1].Set(wx.ACCEL_CTRL, ord("Q"), quitid)
        entries[2].Set(wx.ACCEL_SHIFT, wx.WXK_ESCAPE, quitid)
        accel = wx.AcceleratorTable(entries)
        self.SetAcceleratorTable(accel)

        # ---------------------------------------------------------------------
        # ---------------------------- bind events ----------------------------
        # ---------------------------------------------------------------------
        self.search_view.description.SetValue(
            self.part_info[2] + " " + self.part_info[3] + " " + self.part_info[0]
        )
        self.search_view.description.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.search)
        self.search_view.mpn_textctrl.Bind(wx.EVT_TEXT_ENTER, self.search)
        self.search_view.manufacturer.Bind(wx.EVT_TEXT_ENTER, self.search)
        self.search_view.search_button.Bind(wx.EVT_BUTTON, self.search)

        self.part_list_view.part_list.Bind(
            wx.dataview.EVT_DATAVIEW_COLUMN_HEADER_CLICK, self.OnSortPartList
        )
        self.part_list_view.part_list.Bind(
            wx.dataview.EVT_DATAVIEW_SELECTION_CHANGED, self.on_part_selected
        )
        self.part_list_view.part_list.Bind(
            wx.dataview.EVT_DATAVIEW_ITEM_CONTEXT_MENU, self.on_right_down
        )

        self.part_list_view.prev_button.Bind(wx.EVT_BUTTON, self.on_prev_page)
        self.part_list_view.next_button.Bind(wx.EVT_BUTTON, self.on_next_page)
        self.update_page_label()

        self.part_list_view.select_part_button.Bind(wx.EVT_BUTTON, self.select_part)
        self.part_list_view.select_part_button.SetBitmap(
            loadBitmapScaled(
                "nextpcb-select-part.png",
                # self.parent.scale_factor,
            )
        )

        self.enable_toolbar_buttons(False)
        # ---------------------------------------------------------------------
        # ------------------------------ layout  ------------------------------
        # ---------------------------------------------------------------------
        bSizer2 = wx.BoxSizer(wx.VERTICAL)
        bSizer2.Add(self.search_view, 0, wx.EXPAND, 5)
        bSizer2.Add(self.part_list_view, 1, wx.LEFT | wx.EXPAND, 5)

        bSizer1 = wx.BoxSizer(wx.HORIZONTAL)
        bSizer1.Add(bSizer2, 15, wx.EXPAND | wx.ALL, 5)
        bSizer1.Add(self.part_details_view, 7, wx.EXPAND | wx.ALL, 0)

        layout = wx.BoxSizer(wx.VERTICAL)

        layout.Add(bSizer1, 1, wx.EXPAND, 5)

        self.SetSizer(layout)
        self.Layout()
        self.Centre(wx.BOTH)

    def upadate_settings(self, event):
        """Update the settings on change"""
        wx.PostEvent(
            self.parent,
            UpdateSetting(
                section="partselector",
                setting=event.GetEventObject().GetName(),
                value=event.GetEventObject().GetValue(),
            ),
        )

    @staticmethod
    def get_existing_selection(parts):
        """Check if exactly one LCSC part number is amongst the selected parts."""
        s = set(val for val in parts.values())
        return list(s)[0]

    def quit_dialog(self, e):
        self.Destroy()
        self.EndModal(0)

    def OnSortPartList(self, e):
        """Set order_by to the clicked column and trigger list refresh."""
        self.search(None)

    def enable_toolbar_buttons(self, state):
        """Control the state of all the buttons in toolbar on the right side"""
        for b in [
            self.part_list_view.select_part_button,
        ]:
            b.Enable(bool(state))

    def search(self, e):
        """Search the library for parts that meet the search criteria."""
        if self.current_page == 0:
            self.current_page = 1

        if self.search_view.mpn_textctrl.GetValue() == "":
            mpn = ""
        else:
            mpn = self.search_view.mpn_textctrl.GetValue()
        if self.search_view.manufacturer.GetValue() == "":
            manufacturer = ""
        else:
            manufacturer = self.search_view.manufacturer.GetValue()
        if self.search_view.description.GetValue() == "":
            comment = ""
        else:
            comment = self.search_view.description.GetValue()

        body = [
            {
                "line_no": "10",
                "mpn": mpn,
                "manufacturer": manufacturer,
                "package": "",
                "reference": "",
                "quantity": 0,
                "sku": "",
                "comment": comment,
            }
        ]

        url = "http://192.168.50.100:5010/bom_components_match"
        self.search_view.search_button.Disable()
        try:
            threading.Thread(target=self.search_api_request(url, body)).start()
        finally:
            self.search_view.search_button.Enable()

    def search_api_request(self, url, data):
        wx.CallAfter(wx.BeginBusyCursor)

        headers = {"Content-Type": "application/json"}
        try:
            response = requests.post(url, headers=headers, json=data, timeout=5)
        except Timeout:

            self.report_part_search_error("HTTP response timeout")
        if response.status_code != 200:
            self.report_part_search_error(
                _(f"non-OK HTTP response status：{response.status_code}")
            )
            return
        self.search_part_list = []
        datas = response.json()
        data = datas[0].get("parts", {})
        if not data:
            wx.MessageBox( _("No corresponding data was matched") )
            return
        self.total_num = len(data)
        if self.total_num == 0:
            self.current_page = 0
        for item in data:
            if not item.get("part", {}):
                self.report_part_search_error(
                    _("returned JSON data does not have expected 'part' attribute")
                )
            search_part = item.get("part", {})
            self.search_part_list.append(search_part)
        wx.CallAfter(self.populate_part_list)
        wx.CallAfter(wx.EndBusyCursor)

    def populate_part_list(self):
        """Populate the list with the result of the search."""
        self.part_list_view.part_list.DeleteAllItems()
        if self.search_part_list is None:
            return
        self.total_pages = ceil(self.total_num, 100)
        self.update_page_label()
        self.part_list_view.result_count.SetLabel(_(f"{self.total_num} Results"))
        if self.total_num >= 1000:
            self.part_list_view.result_count.SetLabel(_("1000 Results (limited)" ))
        else:
            self.part_list_view.result_count.SetLabel(f"{self.total_num} Results")

        parameters = ["mpn", "manufacturer", "package", "category"]
        # but "item_total_list" contains more comprehensive data infomation.
        self.item_total_list = []
        for idx, part_info in enumerate(self.search_part_list, start=1):
            part = []
            for k in parameters:
                val = part_info.get(k, "")
                val = "-" if val == "" else val
                part.append(val)
            part.insert(0, f"{idx}")
            manu = part_info.get("manufacturer", {})
            mpn = part_info.get("mpn", {})
            supplier_chain = {}
            headers = {"Content-Type": "application/json"}
            body = [f"-{mpn}"]
            url = "http://192.168.50.102:8012/search/supplychain/list/mfg-mpn"
            response = requests.post(url, headers=headers, json=body, timeout=5)
            if response.status_code != 200:
                self.report_part_search_error(
                    _(f"non-OK HTTP response status：{response.status_code}")
                )
            # judge whether supplier chain data is available
            # Check if the response content is not empty
            if not response.content:
                part.insert(5, "-")
                part.insert(6, "-")
                part.insert(7, "-")
                part.insert(8, "-")
                combined_data = {
                    "part_info": part_info,
                    "supplier_chain": [],
                }
                self.item_total_list.append(combined_data)
                self.part_list_view.part_list.AppendItem(part)
                continue

            datas = response.json()
            supplier_chain = datas[0]
            sku = supplier_chain.get("sku", {})
            sku = "-" if sku == None else sku
            part.insert(5, sku)
            supplier = supplier_chain.get("vendor", {})
            supplier = "-" if supplier == None else supplier
            part.insert(6, supplier)
            if supplier_chain.get("price", {}) == None:
                part.insert(7, "-")
            else:
                price = supplier_chain.get("price", {})[0].get("rmb", {})
                price = "-" if price == "" else price
                part.insert(7, str(price))
            stock = supplier_chain.get("quantity", {})
            stock = "-" if stock == "" else stock
            part.insert(8, str(stock))
            combined_data = {"part_info": part_info, "supplier_chain": supplier_chain}
            self.item_total_list.append(combined_data)
            self.part_list_view.part_list.AppendItem(part)

    def select_part(self, e):
        """Save the selected part number and close the modal."""
        item = self.part_list_view.part_list.GetSelection()
        row = self.part_list_view.part_list.ItemToRow(item)
        if row == -1:
            return
        selection = self.part_list_view.part_list.GetValue(row, 1)
        manu = self.part_list_view.part_list.GetValue(row, 2)
        cate = self.part_list_view.part_list.GetValue(row, 4)
        sku = self.part_list_view.part_list.GetValue(row, 5)
        supp = self.part_list_view.part_list.GetValue(row, 6)
        self.selected_part = self.item_total_list[row]
        evt = AssignPartsEvent(
            mpn=selection,
            manufacturer=manu,
            category=cate,
            sku=sku,
            supplier=supp,
            references=list(self.parts.keys()),
            selected_part_detail=self.selected_part,
        )
        wx.PostEvent(self.parent, evt)
        self.EndModal(wx.ID_OK)

    def on_part_selected(self, e):
        """Enable the toolbar buttons when a selection was made."""
        if self.part_list_view.part_list.GetSelectedItemsCount() > 0:
            self.enable_toolbar_buttons(True)
        else:
            self.enable_toolbar_buttons(False)

        item = self.part_list_view.part_list.GetSelection()
        row = self.part_list_view.part_list.ItemToRow(item)
        if row == -1:
            return
        self.clicked_part = self.item_total_list[row]
        if self.clicked_part != "":
            try:
                wx.BeginBusyCursor()
                self.part_details_view.get_part_data(self.clicked_part)
            finally:
                wx.EndBusyCursor()
        else:
            wx.MessageBox(
                _("Failed to get clicked part from NextPCB"),
                _("Error"),
                style=wx.ICON_ERROR,
            )

    def on_prev_page(self, event):
        self.FindWindowByLabel("0").Destroy()

        if self.current_page > 1:
            self.current_page -= 1
            self.search(None)
            self.update_page_label()

    def on_next_page(self, event):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.search(None)
            self.update_page_label()

    def update_page_label(self):
        self.part_list_view.page_label.SetLabel(
            f"{self.current_page}/{self.total_pages}"
        )

    def help(self, e):
        """Show message box with help instructions"""
        title = _("Help")
        text ="""
        Use % as wildcard selector. \n
        For example DS24% will match DS2411\n
        %QFP% wil match LQFP-64 as well as TQFP-32\n
        The keyword search box is automatically post- and prefixed with wildcard operators.
        The others are not by default.\n
        The keyword search field is applied to "LCSC Part", "Description", "MFR.Part",
        "Package" and "Manufacturer".\n
        Enter triggers the search the same way the search button does.\n
        The results are limited to 1000.
        """
        wx.MessageBox(text, title, style=wx.ICON_INFORMATION)

    def report_part_search_error(self, reason):
        wx.MessageBox(
            _(f"Failed to download part detail from the NextPCB API ({reason})\r\n"),
            _("Error"),
            style=wx.ICON_ERROR,
        )
        wx.CallAfter(wx.EndBusyCursor)
        wx.CallAfter(self.search_view.search_button.Enable())
        return

    def on_right_down(self, e):
        conMenu = wx.Menu()
        selcet_part = wx.MenuItem(conMenu, ID_SELECT_PART, _("Select Part") )
        conMenu.Append(selcet_part)
        conMenu.Bind(wx.EVT_MENU, self.select_part, selcet_part)
        item = self.part_list_view.part_list.GetSelection()
        row = self.part_list_view.part_list.ItemToRow(item)
        if row == -1:
            return
        conMenu.Enable(ID_SELECT_PART, True)
        self.part_list_view.part_list.PopupMenu(conMenu)
        conMenu.Destroy()
