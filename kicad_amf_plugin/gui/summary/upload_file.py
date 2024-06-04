import os
from kicad_amf_plugin.kicad.board_manager import BoardManager
import requests
import webbrowser
import json
import wx
from urllib.parse import urlparse, parse_qs, urlencode
from wx.lib.pubsub import pub
from pathlib import Path
import tempfile
from requests.exceptions import Timeout, HTTPError


TIMEOUT_SECONDS = 100

class UploadFile:
    def __init__(self, board_manager: BoardManager, url, forms, smt_order_region, number ):
        self._board_manager = board_manager
        self._url = url
        self._form = forms
        self._number = number
        self.smt_order_region = smt_order_region
        self.project_path = os.path.split(self._board_manager.board.GetFileName())[0]
        
        self.file_path = os.path.join(self.project_path, "nextpcb")
        try:
            Path(self.file_path).mkdir(parents=True, exist_ok=True)
        except PermissionError as e:
            self.file_path = os.path.join(tempfile.gettempdir(), "nextpcb")
        
        self.usa_get_files()
        self.upload_pcbfile()
        self.upload_smtfile()

    def usa_get_files(self):
        self.getdir = os.path.join(self.file_path, "production_files")
        file_list = []
        
        if os.path.exists(self.getdir) and os.path.isdir(self.getdir):
        # Iterate over files in the directory
            for filename in os.listdir(self.getdir):
                file_path = os.path.join(self.getdir, filename)
                if os.path.isfile(file_path):
                    # Add only files to the file_list
                    file_list.append(file_path)

        self.patch_file = next((file for file in file_list if "CPL" in file and "zip" in file), "")
        self.pcb_file = next((file for file in file_list if "GERBER" in file and "zip" in file), "")
        self.bom_file = next((file for file in file_list if "BOM" in file and "csv" in file), "")


    def upload_pcbfile(self):
        form = { "type": "pcbfile" }
        fp = self.request_api( self._url, self.pcb_file, form )
        if fp is not None:
            self.gerber_file_id = fp.get("response_data",{}).get("gerber_file_id",{})



    def upload_smtfile(self):
        form = { "type": "attach" }
        fp = self.request_api( self._url, self.patch_file, form )
        if fp is not None:
            self.other_file_id = fp.get("response_data",{}).get("other_file_id",{})


    def verify_pcb_smt_upload_success(self):
        if self.other_file_id and self.gerber_file_id:
            return True
        else:
            return False
        
    def upload_bomfile(self):
        if self.smt_order_region == 1:
            form = { 'type': 'pcbabomfile',
                    'gerber_file_id': self.gerber_file_id ,
                    'other_file_id': self.other_file_id ,
                    }
        else:
            form = { 'type': 'pcbabomfile',
                    'gerber_file_id': self.gerber_file_id ,
                    'other_file_id': self.other_file_id ,
                    'region': 'jp',
                    }
        fp = self.request_api( self._url, self.bom_file, form )
        if fp is not None:
            redirect = fp.get("response_data",{}).get("redirect",{})
            parsed_url = urlparse(redirect)
            query_params = parse_qs(parsed_url.query)
            
            query_params['bcount'] = [self._number]
            query_params['number'] = [self._number]
            updated_url = parsed_url._replace(query=urlencode(query_params, doseq=True)).geturl()
            return updated_url


    def request_api(self, _url, upload_file, form ):
        rsp = None
        try:
            rsp = requests.post(
                _url,
                files={
                    "file": open(upload_file, 'rb')
                },
                data=form,
                timeout=TIMEOUT_SECONDS   
            )
            rsp.raise_for_status()  # 检查HTTP响应状态
            fp = rsp.json()  # 解析JSON内容
            return fp
        except Timeout as e:
            self.report_part_search_error(_("HTTP request timed out: {error}").format( error=e))
        except HTTPError as e:
            self.report_part_search_error(_("HTTP error occurred: {error}").format(error=e))
        except ValueError as e:
            self.report_part_search_error(_("Failed to parse JSON response: {error}").format(error=e))
        except Exception as e:
            self.report_part_search_error(_("An unexpected HTTP error occurred: {error}").format(error=e))


    def report_part_search_error(self, reason):
        wx.MessageBox(
            _("Failed to request the API:\r\n{reason}.\r\n \r\nPlease try making the request again.\r\n").format(reason=reason),
            _("Error"),
            style=wx.ICON_ERROR,
        )
        return
