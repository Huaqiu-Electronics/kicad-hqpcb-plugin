import wx
import wx.xrc
import logging
import os
import csv
import wx.dataview
import json

from .ui_import_list_panel.import_list_view import ImportListView
from kicad_amf_plugin.kicad_nextpcb_new.nextpcb_tools_view.ui_assigned_part_panel.assigned_part_view import (
    AssignedPartView,
)
from kicad_amf_plugin.kicad_nextpcb_new.import_BOM_view.import_BOM_store import ImportBOMStore
from kicad_amf_plugin.kicad_nextpcb_new.part_selector_view.part_selector import PartSelectorDialog
from kicad_amf_plugin.kicad_nextpcb_new.events import EVT_ASSIGN_PARTS_EVENT
from kicad_amf_plugin.kicad_nextpcb_new.button_id import (
    ID_MANUAL_MATCH,
    ID_REMOVE_PART,
    ID_COPY_MPN,
    ID_PASTE_MPN,
)


class ImportBOMDailog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(
            self,
            parent,
            id=wx.ID_ANY,
            title="Match Native BOM Table",
            pos=wx.DefaultPosition,
            size=wx.Size(1200, 800),
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.MAXIMIZE_BOX,
        )
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        self.logger = logging.getLogger(__name__)
        self.window = wx.Window(self)

        self.import_list_view = ImportListView(self)
        self.assigned_part_view = AssignedPartView(self)
        self.import_BOM_store = ImportBOMStore(self)

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
        # ----------------------------- layout --------------------------------
        # ---------------------------------------------------------------------

        bSizer5 = wx.BoxSizer(wx.VERTICAL)
        bSizer5.Add(self.import_list_view, 2, wx.ALL | wx.EXPAND, 5)
        bSizer5.Add(self.assigned_part_view, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(bSizer5)
        self.Layout()
        self.Centre(wx.BOTH)

        # ---------------------------------------------------------------------
        # ----------------------------- bind event ----------------------------
        # ---------------------------------------------------------------------
        self.Bind(
            wx.EVT_BUTTON, self.import_mappings, self.import_list_view.import_mapping
        )
        self.Bind(
            wx.EVT_BUTTON, self.export_mappings, self.import_list_view.export_mapping
        )
        self.Bind(
            wx.EVT_BUTTON, self.select_part, self.import_list_view.select_part_button
        )
        self.Bind(
            wx.EVT_BUTTON, self.remove_part, self.import_list_view.remove_part_button
        )
        self.Bind(EVT_ASSIGN_PARTS_EVENT, self.assign_parts)

        self.import_list_view.show_list.Bind(
            wx.dataview.EVT_DATAVIEW_SELECTION_CHANGED, self.get_part_details
        )
        self.import_list_view.show_list.Bind(
            wx.dataview.EVT_DATAVIEW_ITEM_CONTEXT_MENU, self.on_right_down
        )

        # self.import_BOM_store.create_import_db()

    def quit_dialog(self, e):
        self.Destroy()
        self.EndModal(0)

    def populate_import_list(self):
        """Populate the list with the import data result."""
        self.import_list_view.show_list.DeleteAllItems()

        lists = self.import_BOM_store.read_parts_by_group_value_footprint()
        if lists is None:
            self.logger.info("empty")
            return
        for idx, list in enumerate(lists, start=1):
            list.insert(0, f"{idx}")
            self.import_list_view.show_list.AppendItem([str(m) for m in list])

    def import_mappings(self, e=None):
        """Dialog to import mappings from a CSV file."""
        with wx.FileDialog(
            self,
            "Import Mapping CSV",
            "",
            "",
            "CSV files (*.csv)|*.csv",
            wx.FD_OPEN | wx.FD_FILE_MUST_EXIST,
        ) as importFileDialog:
            if importFileDialog.ShowModal() == wx.ID_CANCEL:
                return
            path = importFileDialog.GetPath()
            filename = os.path.basename(path)
            self._import_mappings(path)

    def _import_mappings(self, path):
        """mappings import logic"""
        if os.path.isfile(path):
            with open(path, encoding="gbk") as f:
                csvreader = csv.DictReader(
                    f,
                    fieldnames=(
                        "Reference",
                        "Value",
                        "Footprint",
                        "MPN",
                        "Manufacturer",
                        "Category",
                        "SKU",
                        "Supplier",
                        "Quantity",
                    ),
                )
                next(csvreader)
                References_list = []
                self.import_BOM_store.clear_database()
                for row in csvreader:
                    References = row["Reference"].split(",")
                    for ref in References:
                        ref_data = [
                            ref,
                            row["Value"],
                            row["Footprint"],
                            row["MPN"],
                            row["Manufacturer"],
                            row["Category"],
                            row["SKU"],
                            row["Supplier"],
                            row["Quantity"],
                        ]
                        References_list.append(ref_data)

                for ref_data in References_list:
                    self.import_BOM_store.import_mappings_data(ref_data)
            self.populate_import_list()

    def export_mappings(self, e=None):
        """Dialog to export mappings to a CSV file."""
        with wx.FileDialog(
            self,
            "Export Mapping CSV",
            "",
            "mapping",
            "CSV files (*.csv)|*.csv",
            wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
        ) as exportFileDialog:
            if exportFileDialog.ShowModal() == wx.ID_CANCEL:
                return
            path = exportFileDialog.GetPath()
            self._export_mappings(path)

    def _export_mappings(self, path):
        """mappings export logic"""
        with open(path, "w", newline="") as f:
            csvwriter = csv.writer(f, quotechar='"', quoting=csv.QUOTE_ALL)
            csvwriter.writerow(
                [
                    "Reference",
                    "Value",
                    "Footprint",
                    "MPN",
                    "Manufacturer",
                    "Category",
                    "SKU",
                    "Supplier",
                    "Quantity",
                ]
            )
            for m in self.import_BOM_store.read_parts_by_group_value_footprint():
                csvwriter.writerow(
                    [m[0], m[1], m[2], m[3], m[4], m[5], m[6], m[7], m[8]]
                )

    def select_part(self, e):
        """Select a part from the library and assign it to the selected footprint(s)."""
        selection = {}
        for item in self.import_list_view.show_list.GetSelections():
            row = self.import_list_view.show_list.ItemToRow(item)
            # reference = (self.import_list_view.show_list.GetValue(row, 1).split(","))[0]
            reference = self.import_list_view.show_list.GetValue(row, 1)
            value = self.import_list_view.show_list.GetValue(row, 2)
            fp = self.import_list_view.show_list.GetValue(row, 3)
            MPN = self.import_list_view.show_list.GetValue(row, 4)
            Manufacturer = self.import_list_view.show_list.GetValue(row, 5)
            selection[reference] = MPN + "," + Manufacturer + "," + value + "," + fp
        self.logger.debug(f"Create SQLite table for rotations, {selection}")
        try:
            wx.BeginBusyCursor()
            PartSelectorDialog(self, selection).ShowModal()
        finally:
            wx.EndBusyCursor()

    def remove_part(self, e):
        """Remove an assigned Part number."""
        for item in self.import_list_view.show_list.GetSelections():
            row = self.import_list_view.show_list.ItemToRow(item)
            ref = self.import_list_view.show_list.GetTextValue(row, 1)
            mpn = self.import_list_view.show_list.GetTextValue(row, 4)
            if mpn:
                for iter_ref in ref.split(","):
                    if iter_ref:
                        self.import_BOM_store.set_mpn(iter_ref, "")
                        self.import_BOM_store.set_manufacturer(iter_ref, "")
                        self.import_BOM_store.set_category(iter_ref, "")
                        self.import_BOM_store.set_sku(iter_ref, "")
                        self.import_BOM_store.set_part_detail(iter_ref, "")
        self.populate_import_list()

    def assign_parts(self, e):
        """Assign a selected nextPCB number to parts"""
        for reference in e.references:
            self.import_BOM_store.set_multi_mpn(reference, e.mpn)
            self.import_BOM_store.set_multi_manufacturer(reference, e.manufacturer)
            self.import_BOM_store.set_multi_category(reference, e.category)
            self.import_BOM_store.set_multi_sku(reference, e.sku)
            self.import_BOM_store.set_multi_supplier(reference, e.supplier)
            self.import_BOM_store.set_part_detail(reference, e.selected_part_detail)
        self.populate_import_list()

    def get_part_details(self, e):
        """Fetch part details from NextPCB and show them one after another each in a modal."""
        item = self.import_list_view.show_list.GetSelection()
        row = self.import_list_view.show_list.ItemToRow(item)
        mpn = self.import_list_view.show_list.GetTextValue(row, 4)
        if not mpn:
            self.assigned_part_view.initialize_data()
            return
        else:
            ref = self.import_list_view.show_list.GetTextValue(row, 1).split(",")[0]
            part_detail_db = self.import_BOM_store.get_part_detail(ref)
            self.part_detail_db = json.loads(part_detail_db)
            self.assigned_part_view.get_part_data(self.part_detail_db)
        e.Skip()

    def on_right_down(self, e):
        """Right click context menu for action on parts table."""
        conMenu = wx.Menu()
        manual_match = wx.MenuItem(conMenu, ID_MANUAL_MATCH, "Manual Match")
        conMenu.Append(manual_match)
        conMenu.Bind(wx.EVT_MENU, self.select_part, manual_match)
        remove_mpn = wx.MenuItem(conMenu, ID_REMOVE_PART, "Remove Assigned MPN")
        conMenu.Append(remove_mpn)
        conMenu.Bind(wx.EVT_MENU, self.remove_part, remove_mpn)

        item_count = len(self.import_list_view.show_list.GetSelections())
        if item_count > 1:
            conMenu.Enable(ID_MANUAL_MATCH, False)
        else:
            item = self.import_list_view.show_list.GetSelection()
            row = self.import_list_view.show_list.ItemToRow(item)
            if row == -1:
                return
            mpn = self.import_list_view.show_list.GetTextValue(row, 4)
            state = False if not mpn else True
            conMenu.Enable(ID_REMOVE_PART, state)
        self.import_list_view.show_list.PopupMenu(conMenu)
        # destroy to avoid memory leak
        conMenu.Destroy()

    def __del__(self):
        pass
