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
        rsp = requests.post(
            self._url,
            files={
                "file": open(self.pcb_file, 'rb')
            },
            data=form,
        )
        fp = json.loads(rsp.content)
        self.gerber_file_id = fp.get("response_data",{}).get("gerber_file_id",{})
        # return self.gerber_file_id


    def upload_smtfile(self):
        form = { "type": "attach" }
        rsp = requests.post(
            self._url,
            files={
                "file": open(self.patch_file, 'rb')
            },
            data=form,
        )
        fp = json.loads(rsp.content)
        self.other_file_id = fp.get("response_data",{}).get("other_file_id",{})


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
        rsp = requests.post(
            self._url,
            files={
                "file": open(self.bom_file, 'rb')
            },
            data=form,
        )
        fp = json.loads(rsp.content)
        redirect = fp.get("response_data",{}).get("redirect",{})
        parsed_url = urlparse(redirect)
        query_params = parse_qs(parsed_url.query)
        
        query_params['bcount'] = [self._number]
        query_params['number'] = [self._number]
        updated_url = parsed_url._replace(query=urlencode(query_params, doseq=True)).geturl()
        
        return updated_url



