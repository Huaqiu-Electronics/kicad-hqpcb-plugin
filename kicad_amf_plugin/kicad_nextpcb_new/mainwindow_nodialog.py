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
    EVT_UPDATE_SETTING,
    EVT_CACHE_BITMAP_IN_DATABASE,
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
import time
from kicad_amf_plugin.kicad_nextpcb_new.nextpcb_tools_view.foot_print_list_model import FootprintListModel

DB_MPN = 3
DB_MANU = 4
DB_CATE = 5
DB_SKU = 6
DB_PRICE = 7
DB_QUANT = 8
DB_BOM = 9
DB_POS = 10
DB_SIDE = 11


class NextPCBTools:
    def __init__(self, parent, board_manager: BoardManager):
        
        self.BOARD_LOADED = board_manager.board
        self.project_path = os.path.split(self.BOARD_LOADED.GetFileName())[0]
        self.board_name = os.path.split(self.BOARD_LOADED.GetFileName())[1]
        self.schematic_name = f"{self.board_name.split('.')[0]}.kicad_sch"
        self.store = None
        self.settings = None
        self.group_strategy = 0

        self.bom = [
            {
                "reference": "",
                "value": "",
                "footprint": "",
                "MPN": "",
                "manufacturer": "",
                "Category": "",
                "SKU": "",
                "price": "",
                "quantity": "",
                
            }
        ]

        self.last_call_time = 0  # record last time targger 
        self.throttle_interval = 0.4  # set interval

        self.Bind(wx.EVT_BUTTON, self.export_bom, self.match_part_view.export_csv)
        
        self.Bind(wx.EVT_COMBOBOX, self.group_parts, self.cb_group_strategy)
        self.Bind(wx.EVT_TOOL, self.auto_match_parts, self.auto_match_button)
        self.Bind(
            wx.EVT_BUTTON, self.select_part, self.match_part_view.select_part_button
        )
        self.Bind(
            wx.EVT_BUTTON, self.remove_part, self.match_part_view.remove_part_button
        )


        # ---------------------------------------------------------------------
        # ------------------------ Custom Events ------------------------------
        # ---------------------------------------------------------------------
        self.Bind(EVT_MESSAGE_EVENT, self.display_message)
        self.Bind(EVT_ASSIGN_PARTS_EVENT, self.assign_parts)
        self.Bind(EVT_UPDATE_SETTING, self.update_settings)
        self.Bind( EVT_CACHE_BITMAP_IN_DATABASE, self.onCacheBitmapInDatabase )

        self.init_fabrication()
        self.init_store()
        self.init_logger()
        self.auto_match_parts()

    def m_splitter1OnIdle( self, event ):
        window_size = self.m_splitter1.GetSize()
        height = window_size.height
        self.m_splitter1.SetSashPosition( height-220 )
        self.m_splitter1.Unbind( wx.EVT_IDLE )



    @property
    def file_path(self):
        file_path = os.path.join(self.project_path, "nextpcb")
        try:
            Path(file_path).mkdir(parents=True, exist_ok=True)
        except (PermissionError, OSError) as e:
            return os.path.join(tempfile.gettempdir())
        return os.path.join(self.project_path)


    def on_notebook_page_changed(self, e):
        self.selected_page_index = self.notebook.GetSelection()
        if self.selected_page_index == 0:
            self.footprint_list = self.fplist_all
        elif self.selected_page_index == 1:
            self.footprint_list = self.fplist_unmana

        wx.CallAfter(self.populate_footprint_list)

    def quit_dialog(self, e):
        """Destroy dialog on close"""
        self.Destroy()

    def init_store(self):
        """Initialize the store of part assignments"""
        self.store = Store(self, self.file_path, self.BOARD_LOADED)

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
            
            self.bom_match_api_request (unmanaged_parts )

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
        match_lists = []
        request_bodys = []
        for index, batch_part in enumerate(unmanaged_parts):
            batch_part.append( str(index) )
            value = batch_part[1]
            footprint = batch_part[2]
            idx = batch_part[3]
            request_body= {
                    "line_no": idx,
                    "mpn": "",
                    "manufacturer": "",
                    "package": footprint,
                    "reference": "",
                    "quantity": 0,
                    "sku": "",
                    "comment": value,
                }
            request_bodys.append(request_body)

        headers = {"Content-Type": "application/json"}
        
        # body =[{'line_no': '1', 'mpn': '', 'manufacturer': '', 'package': 'LED_D3.0mm', 'reference': '', 'quantity': 0, 'sku': '', 'comment': 'LED'}, {'line_no': '2', 'mpn': '', 'manufacturer': '', 'package': 'DSUB-9_Female_Horizontal_P2.77x2.84mm_EdgePinOffset14.56mm_Housed_MountingHolesOffset15.98mm', 'reference': '', 'quantity': 0, 'sku': '', 'comment': 'DB9FEM'}, {'line_no': '3', 'mpn': '', 'manufacturer': '', 'package': 'LRTDK', 'reference': '', 'quantity': 0, 'sku': '', 'comment': '470ns'}, {'line_no': '4', 'mpn': '', 'manufacturer': '', 'package': 'subclick', 'reference': '', 'quantity': 0, 'sku': '', 'comment': 'BNC'}, {'line_no': '5', 'mpn': '', 'manufacturer': '', 'package': 'PinHeader_1x02_P2.54mm_Vertical', 'reference': '', 'quantity': 0, 'sku': '', 'comment': 'CONN_2'}, {'line_no': '6', 'mpn': '', 'manufacturer': '', 'package': 'PinHeader_1x05_P2.54mm_Vertical', 'reference': '', 'quantity': 0, 'sku': '', 'comment': 'CONN_5'}]
        body = request_bodys
        url = "https://www.eda.cn/api/chiplet/kicad/bomComponentsMatch"
        
        try:
            response = requests.post(url, headers=headers, json=body, timeout = 120)
        except requests.exceptions.Timeout as e:
            self.report_part_search_error(
                _("HTTP request timed out: {error}").format( error=e)
                )
            return
        except requests.exceptions.RequestException as e:
            self.report_part_search_error(
                _("An error occurred during the request: {error}").format(error=e)
            )
            return
        if response.status_code != 200:
            self.report_part_search_error(
                _("non-OK HTTP response status: {status_code}").format(status_code = response.status_code) 
            )
            return
        if not response.json():
            wx.MessageBox( _("No return data"), _("Info"), style=wx.ICON_ERROR )
            return
        data = response.json()
        res_datas = response.json().get("result", {})
        if not res_datas:
            wx.MessageBox( _("No corresponding data was matched. You can try to manually match."), _("Info") )
            return

        request_bodys = []
        for res_data in res_datas:
            for batch_part in unmanaged_parts:
                if res_data.get("source").get("line_no") == batch_part[3] and res_data.get("queryPartVO"):
                    batch_part.append( res_data.get("queryPartVO").get("part", "-") )
                    batch_part.append( res_data.get("resScore", "-") )
                    manu_id = batch_part[4].get("manufacturer_id", {})
                    mpn = batch_part[4].get("mpn", {})
                    
                    body_value = (f"{manu_id}-{mpn}")
                    request_bodys.append(body_value)


        body = request_bodys
        url = "https://www.eda.cn/api/chiplet/kicad/searchSupplyChain"

        try:
            response = requests.post(url, headers=headers, json=body, timeout = 120 )
        except requests.exceptions.Timeout as e:
            self.report_part_search_error(
                _("HTTP request timed out: {error}").format( error=e)
            )
            return
        except requests.exceptions.RequestException as e:
            self.report_part_search_error(
                _("An error occurred during the request: {error}").format(error=e)
            )
            return
        if response.status_code != 200:
            self.report_part_search_error(
                _("non-OK HTTP response status: {status_code}").format(status_code = response.status_code) 
            )
            return

        res_datas = response.json().get("result", {})

        for batch_part in unmanaged_parts:
            match_list = [None, None, None, None, None, None, None, None]
            if len(batch_part) >= 5:
                sku = "-"
                price = "-"
                prices_stair = "-"
                for data in res_datas:
                    if data.get("mpn") ==  batch_part[4].get("mpn") and data.get("vendor") == "hqself":
                        sku = data.get("sku", "-") 
                        prices_stair = data.get("price", "-") 
                        if prices_stair != "-":
                            for index, price_range in enumerate(prices_stair):
                                price = str(price_range["rmb"])
                                price = "-" if price == "0.0" else price
                                break

                        break 
                batch_part[4]["sku"] = sku
                batch_part[4]["price"] = prices_stair

                match_list[0] = batch_part[0]
                match_list[1] = batch_part[4].get("mpn", "-")
                match_list[2] = batch_part[4].get("manufacturer", "-")
                match_list[3] = batch_part[4].get("category", "-")
                match_list[4] = batch_part[4].get("sku", "-")
                match_list[5] = price
                match_list[6] = batch_part[4]
                match_lists.append(match_list)

        self.batch_update_db_match(match_lists)
        # self.populate_footprint_list()
        # wx.MessageBox(
        #     _('The matching is complete. Check the matching result carefully. You can try to manually match the "Unmatched" part.'),
        #     _("Info"),
        #     style=wx.ICON_INFORMATION,
        # )


    def batch_update_db_match(self, matched_lists):
        if matched_lists:
            self.store.set_batch_bom_match(matched_lists)
            
            # threading.Thread(target= self.download_and_cache_image ,args=(matched_lists, ) ).start()


    def download_and_cache_image(self, matched_lists):
        for matched_list in matched_lists :
            image_url  =  matched_list[6].get("image", {})
            if image_url:
                if not image_url.startswith("http:") and not image_url.startswith("https:"):
                    image_url = "https:" + image_url
                self.logger.debug(f"image_count: {image_url}")
                header = {
                    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"    
                }
                content = None
                try:
                    response = requests.get(image_url, headers=header, timeout= 30 )
                    response.raise_for_status()  # Raises an HTTPError for bad responses
                    content = response.content
                except requests.exceptions.RequestException as e:
                    self.logger.error(f"Error downloading image: {e}. attempts: {image_url}")
                
                if content:
                    matched_list[7] = content
        self.store.set_batch_cache_image(matched_lists)


    def generate_fabrication_data(self):
        """Generate fabrication data."""
        self.fabrication.fill_zones()
        self.fabrication.generate_geber(None)
        self.fabrication.generate_excellon()
        self.fabrication.zip_gerber_excellon()
        self.fabrication.generate_cpl()
        self.fabrication.generate_bom()


    def assign_parts(self, e):
        """Assign a selected nextPCB number to parts"""
        if len(e.references) == 1 and isinstance(e.references[0], str):
            detail = e.selected_part_detail
            match_list =[e.mpn, e.manufacturer, e.category, e.sku, e.price, e.selected_part_detail]
            self.store.set_bom_match_ref( e.references[0],match_list )
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
                part[DB_PRICE] = part[DB_PRICE]
                
                part[DB_BOM] = 0 if "0" in part[DB_BOM].split(",") else 1
                part[DB_POS] = 0 if "0" in part[DB_POS].split(",") else 1
                part[DB_SIDE] = (
                    "T/B"
                    if ("top" in part[DB_SIDE]) and ("bottom" in part[DB_SIDE])
                    else (part[DB_SIDE].split(","))[0]
                )
            part[DB_QUANT] = str( part[DB_QUANT] )
            part[DB_BOM] = toogles_dict.get(part[DB_BOM], toogles_dict.get(1))
            part[DB_POS] = toogles_dict.get(part[DB_POS], toogles_dict.get(1))
            if "," not in part[0]:
                side = "top" if fp.GetLayer() == 0 else "bottom"
                self.store.set_part_side(part[0], side)
                part[DB_SIDE] = side
            part.insert(12, "")
            parts.append(part)
        new_parts = []
        for idx, part in enumerate(parts, start=1):
            part.insert(0, f"{idx}")

            if self.selected_page_index == 1 and part[4]:
                continue
            else:
                new_parts.append(part)
        self.FootprintListModel = FootprintListModel( new_parts )
        self.footprint_list.AssociateModel(self.FootprintListModel)
        self.Layout()  


    def on_sort_footprint_list(self, e):
        """Set order_by to the clicked column and trigger list refresh."""
        self.oeder = self.store.set_order_by(e.GetColumn())
        self.populate_footprint_list()


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

    
    def onCacheBitmapInDatabase(self, evt):
        wx.CallAfter( self.store.set_cache_image, self.image_refs, evt.content)



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



    def export_bom(self, e):
        """Generate the bom file."""
        schematic_name = self.board_name.split(".")[0]
        self.parts = self.store.export_parts_by_group()
        temp_dir = os.path.join(self.file_path, "nextpcb")
        bomFileName = "BOM_" + schematic_name + ".csv"
        if len(self.bom) > 0:
            try:
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
                    _("Export BOM file finished. file path : {temp_dir}").format(temp_dir=temp_dir),
                    _("Info"),
                    style=wx.ICON_INFORMATION,
                )
            except (PermissionError, OSError) as e:
                wx.MessageBox(
                    _("Export BOM file error: {e}").format(e=e),
                    _("Error"),
                    style=wx.ICON_ERROR,
                )


    def report_part_search_error(self, reason):
        wx.MessageBox(
            _("Failed to download part detail from the BOM API:\r\n{reasons}\r\nPlease try again later.\r\n").format(reasons=reason),
            _("Error"),
            style=wx.ICON_ERROR,
        )


    def __del__(self):
        pass
