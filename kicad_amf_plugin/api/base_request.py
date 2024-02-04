import dataclasses
import os

@dataclasses.dataclass
class BaseRequest:
    service: str = "pcb"
    region_id: str = "211"  # TODO
    country: str = "211"  # TODO
    express: str = "31"  # TODO


@dataclasses.dataclass
class SmtRequest:
    add_plat_form: str = 4
    patch_file_name: str = ""
    bom_file_name: str = ""
    pcb_file_name: str = ""
    custom_pcb_ban: str = 1
    bom_purchase: str = 1
    
class SmtFiles:
    patch_file: str = ""
    bom_file: str = ""
    pcb_file: str = ""

# class ReadFile:
#     def __init__(self, project_path):
#         self.project_path = project_path
#         self._board_manager = board_manager
#         self.getdir = os.path.join(self.project_path, "nextpcb", "production_files")
#         self.project_path = os.path.split(self._board_manager.board.GetFileName())[0]

#     def get_files(self):
#             file_list = []
            
#             if os.path.exists(self.getdir) and os.path.isdir(self.getdir):
#                 # Iterate over files in the directory
#                 for filename in os.listdir(self.getdir):
#                     file_path = os.path.join(self.getdir, filename)
#                     if os.path.isfile(file_path):
#                         # Add only files to the file_list
#                         file_list.append(file_path)

#             # patch_file = [file for file in file_list if "CPL" in file and "zip" in file]    
#             # pcb_file = [file for file in file_list if "GERBER" in file and "zip" in file]        
#             # bom_file = [file for file in file_list if "BOM" in file and "csv" in file]

#             # Assuming each file type has at most one file
#             patch_file = next((file for file in file_list if "CPL" in file and "zip" in file), "")
#             pcb_file = next((file for file in file_list if "GERBER" in file and "zip" in file), "")
#             bom_file = next((file for file in file_list if "BOM" in file and "csv" in file), "")

#             return SmtRequest(
#             patch_file=patch_file,
#             patch_file_name=os.path.basename(patch_file),
#             bom_file=bom_file,
#             bom_file_name=os.path.basename(bom_file),
#             pcb_file=pcb_file,
#             pcb_file_name=os.path.basename(pcb_file),
#         )
