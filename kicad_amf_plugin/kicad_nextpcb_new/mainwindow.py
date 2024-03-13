from .store import Store
from .settings import SettingsDialog
from .schematicexport import SchematicExport
from .part_selector_view.part_selector import PartSelectorDialog
from .helpers import (
    PLUGIN_PATH,
    GetScaleFactor,
    HighResWxSize,
    get_footprint_by_ref,
    loadBitmapScaled,
)
from .fabrication import Fabrication

import json
import logging
import os
import re
import sys
import csv

import wx
import wx.dataview
import requests
from requests.exceptions import Timeout
import webbrowser
import threading
from pcbnew import GetBuildVersion, ToMM
from .events import (
    EVT_MESSAGE_EVENT,
    EVT_ASSIGN_PARTS_EVENT,
    EVT_POPULATE_FOOTPRINT_LIST_EVENT,
    EVT_UPDATE_SETTING,
)

from pathlib import Path
import tempfile

from kicad_amf_plugin.kicad_nextpcb_new.nextpcb_tools_view.ui_assigned_part_panel.assigned_part_view import (
    AssignedPartView,
)
from kicad_amf_plugin.kicad_nextpcb_new.nextpcb_tools_view.foot_print_list import FootPrintList
from kicad_amf_plugin.kicad_nextpcb_new.nextpcb_tools_view.ui_match_part_panel.match_part_view import (
    MatchPartView,
)
from .button_id import (
    ID_GROUP,
    ID_AUTO_MATCH,
    ID_GENERATE,
    ID_GENERATE_AND_PLACE_ORDER,
    ID_MAPPINGS,
    ID_SETTINGS,
    ID_MANUAL_MATCH,
    ID_REMOVE_PART,
    ID_PART_DETAILS,
    ID_IMPORT_MAPPING,
    ID_COPY_MPN,
    ID_PASTE_MPN,
)

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

from kicad_amf_plugin.kicad.board_manager import BoardManager

DB_MPN = 3
DB_MANU = 4
DB_CATE = 5
DB_SKU = 6
DB_SUPPL = 7
DB_QUANT = 8
DB_BOM = 9
DB_POS = 10
DE_ROT = 11
DB_SIDE = 12


class NextPCBTools(wx.Dialog):
    def __init__(self, parent, board_manager: BoardManager):
        wx.Dialog.__init__(
            self,
            parent,
            id=wx.ID_ANY,
            title=_("NextPCB Tools"),
            pos=wx.DefaultPosition,
            size=wx.Size(1200, 800),
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.MAXIMIZE_BOX,
        )
        
        self.BOARD_LOADED = board_manager.board

        self.KicadBuildVersion = GetBuildVersion()
        self.window = wx.GetTopLevelParent(self)
        self.SetSize(HighResWxSize(self.window, wx.Size(1200, 800)))
        self.scale_factor = GetScaleFactor(self.window)
        self.project_path = os.path.split(self.BOARD_LOADED.GetFileName())[0]
        self.board_name = os.path.split(self.BOARD_LOADED.GetFileName())[1]
        self.schematic_name = f"{self.board_name.split('.')[0]}.kicad_sch"
        self.hide_bom_parts = False
        self.hide_pos_parts = False
        self.manufacturers = []
        self.packages = []
        self.store = None
        self.settings = None
        self.group_strategy = 0
        self.load_settings()
        self.Bind(wx.EVT_CLOSE, self.quit_dialog)

        self.assigned_part_view = AssignedPartView(self)
        self.match_part_view = MatchPartView(self)

        # ---------------------------------------------------------------------
        # ---------------------------- events --------------------------------
        # ---------------------------------------------------------------------
        self.bom = [
            {
                "reference": "",
                "value": "",
                "footprint": "",
                "MPN": "",
                "manufacturer": "",
                "Category": "",
                "SKU": "",
                "supplier": "",
                "quantity": "",
            }
        ]
        self.Bind(wx.EVT_BUTTON, self.export_bom, self.match_part_view.export_csv)
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
        # -------------------- Horizontal top buttons -------------------------
        # ---------------------------------------------------------------------

        self.upper_toolbar = wx.ToolBar(
            self,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.Size(1400, -1),
            wx.TB_HORIZONTAL | wx.TB_TEXT | wx.TB_HORZ_LAYOUT | wx.TB_NODIVIDER,
        )
        self.upper_toolbar.SetToolBitmapSize((24, 24))
        self.group_label = wx.StaticText(
            self.upper_toolbar, wx.ID_ANY, label=_(" Group by: ")
        )

        self.group_label.Wrap(-1)
        self.upper_toolbar.AddControl(self.group_label)

        self.upper_toolbar.AddSeparator()

        group_strategy_value = [_(" No Group "), _(" Value & Footprint ")]

        self.cb_group_strategy = wx.ComboBox(
            self.upper_toolbar,
            ID_GROUP,
            _("No Group"),
            wx.DefaultPosition,
            wx.DefaultSize,
            group_strategy_value,
            style=wx.CB_DROPDOWN | wx.CB_READONLY,
        )

        self.cb_group_strategy.SetSelection(0)

        self.upper_toolbar.AddControl(self.cb_group_strategy)

        self.upper_toolbar.AddSeparator()

        self.auto_match_button = self.upper_toolbar.AddTool(
            ID_AUTO_MATCH,
            _("Auto Match "),
            loadBitmapScaled("nextpcb-automatch.png", 1.2),
            _("Auto Match MPN number to parts"),
        )
        self.upper_toolbar.AddStretchableSpace()

        self.generate_button = wx.Button(
            self.upper_toolbar,
            ID_GENERATE,
            _(" Generate "),
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.generate_button.SetToolTip(
            wx.ToolTip( _("Generate fabrication files to the project folder") )
        )
        self.upper_toolbar.AddControl(self.generate_button)
        self.upper_toolbar.SetToolLongHelp(
            ID_GENERATE, _("Generate fabrication files")
        )


        self.settings_button = self.upper_toolbar.AddTool(
            ID_SETTINGS,
            "",
            loadBitmapScaled("nextpcb-setting.png", self.scale_factor),
            _("Settings"),
        )

        self.upper_toolbar.Realize()

        self.Bind(wx.EVT_COMBOBOX, self.group_parts, self.cb_group_strategy)
        self.Bind(wx.EVT_TOOL, self.auto_match_parts, self.auto_match_button)
        self.Bind(wx.EVT_BUTTON, self.generate_fabrication_file, self.generate_button)
        self.Bind(wx.EVT_TOOL, self.manage_settings, self.settings_button)

        # ---------------------------------------------------------------------
        # ------------------ down toolbar List --------------------------
        # ---------------------------------------------------------------------

        self.Bind(
            wx.EVT_BUTTON, self.select_part, self.match_part_view.select_part_button
        )
        self.Bind(
            wx.EVT_BUTTON, self.remove_part, self.match_part_view.remove_part_button
        )

        # ---------------------------------------------------------------------
        # ----------------------- Footprint List ------------------------------
        # ---------------------------------------------------------------------
        table_sizer = wx.BoxSizer(wx.VERTICAL)
        table_sizer.SetMinSize(HighResWxSize(self.window, wx.Size(-1, 300)))

        self.notebook = wx.Notebook(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.first_panel = wx.Panel(
            self.notebook,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TAB_TRAVERSAL,
        )
        self.first_panel.Layout()
        self.notebook.AddPage(self.first_panel, _("   All   "), True)
        grid_sizer1 = wx.GridSizer(0, 1, 0, 0)
        self.first_panel.SetSizer(grid_sizer1)
        grid_sizer1.Fit(self.first_panel)
        self.fplist_all = FootPrintList(self.first_panel, self)
        grid_sizer1.Add(self.fplist_all, 20, wx.ALL | wx.EXPAND, 5)
        self.selected_page_index = 0

        self.second_panel = wx.Panel(
            self.notebook,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TAB_TRAVERSAL,
        )
        self.second_panel.Layout()
        self.notebook.AddPage(self.second_panel,_("Unmanaged"), False)
        grid_sizer2 = wx.GridSizer(0, 1, 0, 0)
        grid_sizer2.Fit(self.second_panel)
        self.second_panel.SetSizer(grid_sizer2)
        self.fplist_unmana = FootPrintList(self.second_panel, self)
        grid_sizer2.Add(self.fplist_unmana, 20, wx.ALL | wx.EXPAND, 5)

        table_sizer.Add(self.notebook, 20, wx.EXPAND | wx.ALL, 5)
        table_sizer.Add(self.match_part_view, 0, wx.ALL | wx.EXPAND, 0)

        self.notebook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.on_notebook_page_changed)
        self.notebook.Bind(
            wx.dataview.EVT_DATAVIEW_COLUMN_HEADER_CLICK, self.on_sort_footprint_list
        )
        self.notebook.Bind(
            wx.dataview.EVT_DATAVIEW_SELECTION_CHANGED, self.get_part_details
        )
        self.notebook.Bind(
            wx.dataview.EVT_DATAVIEW_ITEM_ACTIVATED, self.get_part_details
        )
        self.notebook.Bind(wx.dataview.EVT_DATAVIEW_ITEM_CONTEXT_MENU, self.OnRightDown)
        self.notebook.Bind(
            wx.dataview.EVT_DATAVIEW_ITEM_VALUE_CHANGED, self.toggle_update_to_db
        )

        # ---------------------------------------------------------------------
        # ---------------------- Main Layout Sizer ----------------------------
        # ---------------------------------------------------------------------
        self.assigned_part = wx.BoxSizer(wx.VERTICAL)
        self.assigned_part.SetMinSize(wx.Size(-1, 220))
        self.assigned_part.Add(self.assigned_part_view, 1, wx.EXPAND, 0)

        self.SetSizeHints(HighResWxSize(self.window, wx.Size(1000, -1)), wx.DefaultSize)
        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(self.upper_toolbar, 0, wx.ALL | wx.EXPAND, 5)
        layout.Add(table_sizer, 5, wx.ALL | wx.EXPAND, 5)
        layout.Add(self.assigned_part, 2, wx.ALL | wx.EXPAND, 0)

        self.SetSizer(layout)
        self.Layout()
        self.Centre(wx.BOTH)

        # ---------------------------------------------------------------------
        # ------------------------ Custom Events ------------------------------
        # ---------------------------------------------------------------------
        self.Bind(EVT_MESSAGE_EVENT, self.display_message)
        self.Bind(EVT_ASSIGN_PARTS_EVENT, self.assign_parts)
        self.Bind(EVT_POPULATE_FOOTPRINT_LIST_EVENT, self.populate_footprint_list)
        self.Bind(EVT_UPDATE_SETTING, self.update_settings)

        self.init_logger()
        self.on_notebook_page_changed(None)
        self.init_fabrication()
        self.init_store()

    @property
    def file_path(self):
        file_path = os.path.join(self.project_path, "nextpcb")
        try:
            Path(file_path).mkdir(parents=True, exist_ok=True)
        except PermissionError as e:
            return os.path.join(tempfile.gettempdir())
        return os.path.join(self.project_path)


    def on_notebook_page_changed(self, e):
        self.selected_page_index = self.notebook.GetSelection()
        if self.selected_page_index == 0:
            self.footprint_list = self.fplist_all
        elif self.selected_page_index == 1:
            self.footprint_list = self.fplist_unmana

        self.populate_footprint_list()

    def quit_dialog(self, e):
        """Destroy dialog on close"""
        self.Destroy()

    def init_store(self):
        """Initialize the store of part assignments"""
        self.store = Store(self, self.file_path, self.BOARD_LOADED)
        self.populate_footprint_list()

    def init_fabrication(self):
        """Initialize the fabrication"""
        self.fabrication = Fabrication(self, self.BOARD_LOADED, self.file_path)

    def group_parts(self, e):
        """ """
        if self.group_strategy != self.cb_group_strategy.GetSelection():
            self.group_strategy = self.cb_group_strategy.GetSelection()
            self.populate_footprint_list()

    def get_display_parts(self):
        """ """
        parts = []
        if self.group_strategy == 0:
            parts = self.store.read_all()
        elif self.group_strategy == 1:
            parts = self.store.read_parts_by_group_value_footprint()
        return parts

    def auto_match_parts(self, e):
        self.upper_toolbar.EnableTool(ID_AUTO_MATCH, False)
        try:
            wx.BeginBusyCursor()
            # get unmanaged part from UI
            unmanaged_parts = self.get_unmanaged_parts_from_list()

            thread = threading.Thread(
                target=self.bom_match_api_request(unmanaged_parts)
            )
            thread.start()
            thread.join()

            # self.update_db_after_match()

            self.populate_footprint_list()
            wx.MessageBox(
                _("Auto match finished.Some parts might match failed. You can try it again or match by manual."),
                _("Info"),
                style=wx.ICON_INFORMATION,
            )
        finally:
            wx.EndBusyCursor()
            self.upper_toolbar.EnableTool(ID_AUTO_MATCH, True)

    def get_unmanaged_parts_from_list(self):
        rows = []
        parts = self.store.read_parts_by_group_value_footprint()
        for part in parts:
            ref = part[0]
            val = part[1]
            fp = part[2]
            mpn = part[3]
            if not mpn:
                row = [ref, val, fp]
                rows.append(row)
        return rows

    def bom_match_api_request(self, unmanaged_parts):

        start = 0
        batch_size = 1
        self.matched_list = [None, None, None, None, None]
        while start < len(unmanaged_parts):
            temp_list = [None, None, None, None, None, None]
            batch_parts = unmanaged_parts[start]
            start += batch_size
            references = batch_parts[0]
            value = batch_parts[1]
            footprint = batch_parts[2]

            headers = {"Content-Type": "application/json"}
            body = [
                {
                    "line_no": "10",
                    "mpn": "",
                    "manufacturer": "",
                    "package": footprint,
                    "reference": "",
                    "quantity": 0,
                    "sku": "",
                    "comment": value,
                }
            ]
            url = "http://192.168.50.100:5010/bom_components_match"

            response = requests.post(url, headers=headers, json=body)
            if response.status_code != 200:
                wx.MessageBox(
                    _(f"non-OK HTTP response.status code:{response.status_code}"),
                    _("Error"),
                    style=wx.ICON_ERROR,
                )
                continue

            rsp_datas = response.json()

            if not rsp_datas:
                continue
            rsp_data = rsp_datas[0].get("parts", {})
            if not rsp_data:
                continue
            if not rsp_data[0].get("part", {}):
                continue
            BOM_part = rsp_data[0].get("part", {})

            manu = BOM_part.get("manufacturer", {})
            mpn = BOM_part.get("mpn", {})
            supplier_chain = {}
            headers = {"Content-Type": "application/json"}
            body = [f"-{mpn}"]
            url = "http://192.168.50.102:8012/search/supplychain/list/mfg-mpn"
            response = requests.post(url, headers=headers, json=body, timeout=5)

            if not response.content:
                temp_list[3] = "-"
                temp_list[4] = "-"
                combined_data = {
                    "part_info": BOM_part,
                    "supplier_chain": [],
                }
            else:
                datas = response.json()
                supplier_chain = datas[0]
                sku = supplier_chain.get("sku", {})
                sku = "-" if sku == "" else sku
                temp_list[3] = supplier_chain.get("sku", {})
                supplier = supplier_chain.get("sku", {})
                supplier = "-" if supplier == "" else supplier
                temp_list[4] = supplier_chain.get("vendor", {})
                combined_data = {
                    "part_info": BOM_part,
                    "supplier_chain": supplier_chain,
                }

            temp_list[0] = BOM_part.get("mpn", {})
            temp_list[1] = BOM_part.get("manufacturer", {})
            temp_list[2] = BOM_part.get("category", {})
            temp_list[5] = combined_data
            self.update_db_after_match(references, temp_list)
            self.populate_footprint_list()

    def update_db_after_match(self, references, matched_list):
        if matched_list:
            # for i in matched_list:
            for reference in references.split(","):
                self.store.set_mpn(reference, matched_list[0])
                self.store.set_manufacturer(reference, matched_list[1])
                self.store.set_category(reference, matched_list[2])
                self.store.set_sku(reference, matched_list[3])
                self.store.set_supplier(reference, matched_list[4])
                self.store.set_part_detail(reference, matched_list[5])

    def generate_fabrication_data(self, e):
        """Generate fabrication data."""
        self.fabrication.fill_zones()
        self.fabrication.generate_geber(None)
        self.fabrication.generate_excellon()
        self.fabrication.zip_gerber_excellon()
        self.fabrication.generate_cpl()
        self.fabrication.generate_bom()

    def generate_fabrication_file(self, e):
        """Generate fabrication data."""
        self.generate_fabrication_data(e)
        self.fabrication.path_message()

    def assign_parts(self, e):
        """Assign a selected nextPCB number to parts"""
        if len(e.references) == 1 and isinstance(e.references[0], str):
            references_list = e.references[0].split(",")
            for reference in references_list:
                self.store.set_mpn(reference, e.mpn)
                self.store.set_manufacturer(reference, e.manufacturer)
                self.store.set_category(reference, e.category)
                self.store.set_sku(reference, e.sku)
                self.store.set_supplier(reference, e.supplier)
                self.store.set_part_detail(reference, e.selected_part_detail)
        self.populate_footprint_list()

    def display_message(self, e):
        """Dispaly a message with the data from the event"""
        styles = {
            "info": wx.ICON_INFORMATION,
            "warning": wx.ICON_WARNING,
            "error": wx.ICON_ERROR,
        }
        wx.MessageBox(e.text, e.title, style=styles.get(e.style, wx.ICON_INFORMATION))

    def populate_footprint_list(self, e=None):
        """Populate/Refresh list of footprints."""
        if not self.store:
            self.init_store()
        self.footprint_list.DeleteAllItems()
        toogles_dict = {
            0: False,
            1: True,
            "0": False,
            "1": True,
        }
        numbers = []
        parts = []
        display_parts = self.get_display_parts()
        for part in display_parts:
            fp = get_footprint_by_ref(self.BOARD_LOADED, (part[0].split(","))[0])[0]
            # ---Get rid of hardcoded numbers and so on and replace them with macros or key-value pairs--
            if part[DB_MPN] and part[DB_MPN] not in numbers:
                numbers.append(part[DB_MPN])
            if "," in part[0]:
                part[DB_MANU] = (part[DB_MANU].split(","))[0]
                part[DB_CATE] = (part[DB_CATE].split(","))[0]
                part[DB_SKU] = part[DB_SKU]
                part[DB_SUPPL] = part[DB_SUPPL]
                part[DB_QUANT] = part[DB_QUANT]
                part[DB_BOM] = 0 if "0" in part[DB_BOM].split(",") else 1
                part[DB_POS] = 0 if "0" in part[DB_POS].split(",") else 1
                part[DE_ROT] = ""
                part[DB_SIDE] = (
                    "T/B"
                    if ("top" in part[DB_SIDE]) and ("bottom" in part[DB_SIDE])
                    else (part[DB_SIDE].split(","))[0]
                )
            part[DB_BOM] = toogles_dict.get(part[DB_BOM], toogles_dict.get(1))
            part[DB_POS] = toogles_dict.get(part[DB_POS], toogles_dict.get(1))
            if "," not in part[0]:
                side = "top" if fp.GetLayer() == 0 else "bottom"
                self.store.set_part_side(part[0], side)
                part[DB_SIDE] = side
            part.insert(13, "")
            parts.append(part)
        for idx, part in enumerate(parts, start=1):
            part.insert(0, f"{idx}")
            part[9] = str(part[9])
            if self.selected_page_index == 1 and part[4]:
                continue
            self.listsd = self.footprint_list.AppendItem(part)

    def on_sort_footprint_list(self, e):
        """Set order_by to the clicked column and trigger list refresh."""
        self.oeder = self.store.set_order_by(e.GetColumn())
        self.populate_footprint_list()

    def enable_all_buttons(self, state):
        """Control state of all the buttons"""
        self.enable_top_buttons(state)

    def enable_top_buttons(self, state):
        """Control the state of all the buttons in the top section"""
        for button in (
            ID_GROUP,
            ID_AUTO_MATCH,
            ID_GENERATE,
            ID_GENERATE_AND_PLACE_ORDER,
            ID_MAPPINGS,
            ID_SETTINGS,
        ):
            self.upper_toolbar.EnableTool(button, state)

    def toggle_bom(self, e):
        """Toggle the exclude from BOM attribute of a footprint."""
        selected_rows = []
        for item in self.footprint_list.GetSelections():
            row = self.footprint_list.ItemToRow(item)
            selected_rows.append(row)
            refs = self.footprint_list.GetTextValue(row, 1).split(",")
            for ref in refs:
                bom = self.footprint_list.GetValue(row, 10)
                self.store.set_bom(ref, bom)
        self.populate_footprint_list()
        for row in selected_rows:
            self.footprint_list.SelectRow(row)

    def toggle_pos(self, e):
        """Toggle the exclude from POS attribute of a footprint."""
        selected_rows = []
        for item in self.footprint_list.GetSelections():
            row = self.footprint_list.ItemToRow(item)
            selected_rows.append(row)
            refs = self.footprint_list.GetTextValue(row, 1).split(",")
            for ref in refs:
                pos = self.footprint_list.GetValue(row, 11)
                self.store.set_pos(ref, pos)
        self.populate_footprint_list()
        for row in selected_rows:
            self.footprint_list.SelectRow(row)

    def remove_part(self, e):
        """Remove an assigned a Part number to a footprint."""
        for item in self.footprint_list.GetSelections():
            row = self.footprint_list.ItemToRow(item)
            ref = self.footprint_list.GetTextValue(row, 1)
            mpn = self.footprint_list.GetTextValue(row, 4)
            if mpn:
                for iter_ref in ref.split(","):
                    if iter_ref:
                        self.store.set_mpn(iter_ref, "")
                        self.store.set_manufacturer(iter_ref, "")
                        self.store.set_category(iter_ref, "")
                        self.store.set_sku(iter_ref, "")
                        self.store.set_supplier(iter_ref, "")
                        self.store.set_bom(iter_ref, True)
                        self.store.set_pos(iter_ref, True)
                        self.store.set_part_detail(iter_ref, "")
        self.populate_footprint_list()

    def select_alike(self, e):
        """Select all parts that have the same value and footprint."""
        num_sel = self.footprint_list.GetSelectedItemsCount()
        # could have selected more than 1 item (by mistake?)
        if num_sel == 1:
            item = self.footprint_list.GetSelection()
        else:
            self.logger.warning("Select only one component, please.")
            return
        row = self.footprint_list.ItemToRow(item)
        ref = self.footprint_list.GetValue(row, 1)
        part = self.store.get_part(ref)
        for r in range(self.footprint_list.GetItemCount()):
            value = self.footprint_list.GetValue(r, 2)
            fp = self.footprint_list.GetValue(r, 3)
            if part[1] == value and part[2] == fp:
                self.footprint_list.SelectRow(r)

    def get_part_details(self, e):
        """Fetch part details from NextPCB and show them one after another each in a modal."""
        item = self.footprint_list.GetSelection()
        row = self.footprint_list.ItemToRow(item)
        mpn = self.footprint_list.GetTextValue(row, 4)
        if not mpn:
            self.assigned_part_view.initialize_data()
            return
        else:
            ref = self.footprint_list.GetTextValue(row, 1).split(",")[0]
            part_detail_db = self.store.get_part_detail(ref)
            self.part_detail_db = json.loads(part_detail_db)
            self.assigned_part_view.get_part_data(self.part_detail_db)
        e.Skip()

    def get_column_by_name(self, column_title_to_find):
        """Lookup a column in our main footprint table by matching its title"""
        for col in self.footprint_list.Columns:
            if col.Title == column_title_to_find:
                return col
        return None

    def get_column_position_by_name(self, column_title_to_find):
        """Lookup the index of a column in our main footprint table by matching its title"""
        col = self.get_column_by_name(column_title_to_find)
        if not col:
            return -1
        return self.footprint_list.GetColumnPosition(col)


    def get_row_item_in_column(self, row, column_title):
        return self.footprint_list.GetTextValue(
            row, self.get_column_position_by_name(column_title)
        )

    def manage_settings(self, e=None):
        """Manage settings."""
        SettingsDialog(self).ShowModal()

    def update_settings(self, e):
        """Update the settings on change"""
        if e.section not in self.settings:
            self.settings[e.section] = {}
        self.settings[e.section][e.setting] = e.value
        self.save_settings()

    def load_settings(self):
        """Load settings from settings.json"""
        with open(os.path.join(PLUGIN_PATH, "settings.json")) as j:
            self.settings = json.load(j)

    def save_settings(self):
        """Save settings to settings.json"""
        with open(os.path.join(PLUGIN_PATH, "settings.json"), "w") as j:
            json.dump(self.settings, j)

    def calculate_costs(self, e):
        """Hopefully we will be able to calculate the part costs in the future."""
        pass

    def select_part(self, e):
        """Select a part from the library and assign it to the selected footprint(s)."""
        selection = {}
        for item in self.footprint_list.GetSelections():
            row = self.footprint_list.ItemToRow(item)
            reference = self.footprint_list.GetValue(row, 1)
            value = self.footprint_list.GetValue(row, 2)
            fp = self.footprint_list.GetValue(row, 3)
            MPN = self.footprint_list.GetValue(row, 4)
            Manufacturer = self.footprint_list.GetValue(row, 5)
            selection[reference] = MPN + "," + Manufacturer + "," + value + "," + fp
        self.logger.debug(f"Create SQLite table for rotations, {selection}")
        try:
            wx.BeginBusyCursor()
            PartSelectorDialog(self, selection).ShowModal()
        finally:
            wx.EndBusyCursor()

    def copy_part_lcsc(self, e):
        """Fetch part details from and show them in a modal."""

        item = self.footprint_list.GetSelection()
        row = self.footprint_list.ItemToRow(item)
        if row == -1:
            return
        part = ""
        part += str(self.footprint_list.GetTextValue(row, 4)) + "\n"
        part += str(self.footprint_list.GetTextValue(row, 5)) + "\n"
        part += str(self.footprint_list.GetTextValue(row, 6)) + "\n"
        part += str(self.footprint_list.GetTextValue(row, 7)) + "\n"
        part += str(self.footprint_list.GetTextValue(row, 8)) + "\n"
        ref = self.footprint_list.GetTextValue(row, 1).split(",")[0]
        part += str(self.store.get_part_detail(ref))

        if part != "":
            if wx.TheClipboard.Open():
                wx.TheClipboard.SetData(wx.TextDataObject(part))
                wx.TheClipboard.Close()

    def paste_part_lcsc(self, e):
        text_data = wx.TextDataObject()
        if wx.TheClipboard.Open():
            success = wx.TheClipboard.GetData(text_data)
            wx.TheClipboard.Close()
        if success:
            lines = text_data.GetText().split("\n")
            mpn = lines[0]
            manufacturer = lines[1]
            cate = lines[2]
            sku = lines[3]
            supplier = lines[4]
            part_detail = json.loads(lines[5])

            if mpn == "":
                return
            item = self.footprint_list.GetSelection()
            row = self.footprint_list.ItemToRow(item)
            references = self.footprint_list.GetTextValue(row, 1)
            for ref in references.split(","):
                self.store.set_mpn(ref, mpn)
                self.store.set_manufacturer(ref, manufacturer)
                self.store.set_category(ref, cate)
                self.store.set_sku(ref, sku)
                self.store.set_supplier(ref, supplier)
                self.store.set_part_detail(ref, part_detail)
        self.populate_footprint_list()

    def export_to_schematic(self, e):
        """Dialog to select schematics."""
        with wx.FileDialog(
            self,
            "Select Schematics",
            self.project_path,
            self.schematic_name,
            "KiCad V6 Schematics (*.kicad_sch)|*.kicad_sch",
            wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE,
        ) as openFileDialog:
            if openFileDialog.ShowModal() == wx.ID_CANCEL:
                return
            paths = openFileDialog.GetPaths()
            SchematicExport(self).load_schematic(paths)

    def sanitize_lcsc(self, lcsc_PN):
        m = re.search("C\\d+", lcsc_PN, re.IGNORECASE)
        if m:
            return m.group(0)
        return ""

    def OnRightDown(self, e):
        """Right click context menu for action on parts table."""
        conMenu = wx.Menu()
        copy_lcsc = wx.MenuItem(conMenu, ID_COPY_MPN, _("Copy MPN"))
        conMenu.Append(copy_lcsc)
        conMenu.Bind(wx.EVT_MENU, self.copy_part_lcsc, copy_lcsc)

        paste_lcsc = wx.MenuItem(conMenu, ID_PASTE_MPN, _("Paste MPN"))
        conMenu.Append(paste_lcsc)
        conMenu.Bind(wx.EVT_MENU, self.paste_part_lcsc, paste_lcsc)

        manual_match = wx.MenuItem(conMenu, ID_MANUAL_MATCH, _("Manual Match"))
        conMenu.Append(manual_match)
        conMenu.Bind(wx.EVT_MENU, self.select_part, manual_match)

        remove_mpn = wx.MenuItem(conMenu, ID_REMOVE_PART, _("Remove Assigned MPN"))
        conMenu.Append(remove_mpn)
        conMenu.Bind(wx.EVT_MENU, self.remove_part, remove_mpn)

        part_detail = wx.MenuItem(conMenu, ID_PART_DETAILS, _("Show Part Details"))
        conMenu.Append(part_detail)

        item_count = len(self.footprint_list.GetSelections())
        if item_count > 1:
            for menu_item in (
                ID_COPY_MPN,
                ID_PASTE_MPN,
                ID_MANUAL_MATCH,
                ID_PART_DETAILS,
            ):
                conMenu.Enable(menu_item, False)
        else:
            item = self.footprint_list.GetSelection()
            row = self.footprint_list.ItemToRow(item)
            if row == -1:
                return
            mpn = self.footprint_list.GetTextValue(row, 4)
            state = False if not mpn else True

            for menu_item in (ID_COPY_MPN, ID_REMOVE_PART, ID_PART_DETAILS):
                conMenu.Enable(menu_item, state)
        self.footprint_list.PopupMenu(conMenu)
        # destroy to avoid memory leak
        conMenu.Destroy()

    def toggle_update_to_db(self, e):
        col = e.GetColumn()

        if col == 10:
            self.toggle_bom(e)
        elif col == 11:
            self.toggle_pos(e)
        else:
            pass

    def init_logger(self):
        """Initialize logger to log into textbox"""
        root = logging.getLogger()
        root.setLevel(logging.DEBUG)
        # Log to stderr
        handler1 = logging.StreamHandler(sys.stderr)
        handler1.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(funcName)s -  %(message)s",
            datefmt="%Y.%m.%d %H:%M:%S",
        )
        handler1.setFormatter(formatter)
        root.addHandler(handler1)
        self.logger = logging.getLogger(__name__)


    def export_bom(self, e):
        """Generate the bom file."""
        self.schematic_name = self.board_name.split(".")[0]
        self.parts = self.store.export_parts_by_group()
        temp_dir = os.path.join(self.file_path, "nextpcb")
        bomFileName = "BOM_" + self.schematic_name + ".csv"
        if len(self.bom) > 0:
            with open(
                (os.path.join(temp_dir, bomFileName)),
                "w",
                newline="",
                encoding="utf-8-sig",
            ) as outfile:
                csv_writer = csv.writer(outfile)
                # writing headers of CSV file
                csv_writer.writerow(self.bom[0].keys())
                # Output all of the component information
                for component in self.parts:
                    csv_writer.writerow(component)
            wx.MessageBox(
                _(f"Export BOM file finished. file path : {temp_dir}"),
                _("Info"),
                style=wx.ICON_INFORMATION,
            )

    def __del__(self):
        pass
