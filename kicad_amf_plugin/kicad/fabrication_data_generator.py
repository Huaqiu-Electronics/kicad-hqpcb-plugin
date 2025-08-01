# Inspired by https://github.com/Bouni/kicad-jlcpcb-tools

import csv
import logging
import os
import re
from pathlib import Path
from zipfile import ZipFile
import contextlib
import shutil
import tempfile

from pcbnew import (
    EXCELLON_WRITER,
    PCB_PLOT_PARAMS,
    PLOT_CONTROLLER,
    PLOT_FORMAT_GERBER,
    ZONE_FILLER,
    B_Cu,
    B_Mask,
    B_Paste,
    B_SilkS,
    Cmts_User,
    Edge_Cuts,
    F_Cu,
    F_Mask,
    F_Paste,
    F_SilkS,
    GetBoard,
    GetBuildVersion,
    In1_Cu,
    In2_Cu,
    In3_Cu,
    In4_Cu,
    ToMM,
)

from .helpers import get_exclude_from_pos, get_footprint_by_ref, get_smd, is_nightly

from enum import IntEnum
class PCB_LAYER_ID(IntEnum):
    UNDEFINED_LAYER = -1
    UNSELECTED_LAYER = -2
    F_Cu = 0
    B_Cu = 2
    In1_Cu = 4
    In2_Cu = 6
    In3_Cu = 8
    In4_Cu = 10
    In5_Cu = 12
    In6_Cu = 14
    In7_Cu = 16
    In8_Cu = 18
    In9_Cu = 20
    In10_Cu = 22
    In11_Cu = 24
    In12_Cu = 26
    In13_Cu = 28
    In14_Cu = 30
    In15_Cu = 32
    In16_Cu = 34
    In17_Cu = 36
    In18_Cu = 38
    In19_Cu = 40
    In20_Cu = 42
    In21_Cu = 44
    In22_Cu = 46
    In23_Cu = 48
    In24_Cu = 50
    In25_Cu = 52
    In26_Cu = 54
    In27_Cu = 56
    In28_Cu = 58
    In29_Cu = 60
    In30_Cu = 62


plot_CuIn = [
                    ("CuIn1", PCB_LAYER_ID.In1_Cu, "Inner layer 1"  ) ,
                    ("CuIn2", PCB_LAYER_ID.In2_Cu, "Inner layer 2"  ) ,
                    ("CuIn3", PCB_LAYER_ID.In3_Cu, "Inner layer 3"  ) ,
                    ("CuIn4", PCB_LAYER_ID.In4_Cu, "Inner layer 4"  ) ,
                    ("CuIn5", PCB_LAYER_ID.In5_Cu, "Inner layer 5"  ) ,
                    ("CuIn6", PCB_LAYER_ID.In6_Cu, "Inner layer 6"  ) ,
                    ("CuIn7", PCB_LAYER_ID.In7_Cu, "Inner layer 7"  ) ,
                    ("CuIn8", PCB_LAYER_ID.In8_Cu, "Inner layer 8"  ) ,
                    ("CuIn9", PCB_LAYER_ID.In9_Cu, "Inner layer 9"  ) ,
                    ("CuIn10", PCB_LAYER_ID.In10_Cu, "Inner layer 10" ) ,   
                    ("CuIn11", PCB_LAYER_ID.In11_Cu, "Inner layer 11"  ) ,
                    ("CuIn12", PCB_LAYER_ID.In12_Cu, "Inner layer 12"  ) ,
                    ("CuIn13", PCB_LAYER_ID.In13_Cu, "Inner layer 13"  ) ,
                    ("CuIn14", PCB_LAYER_ID.In14_Cu, "Inner layer 14"  ) ,
                    ("CuIn15", PCB_LAYER_ID.In15_Cu, "Inner layer 15"  ) ,
                    ("CuIn16", PCB_LAYER_ID.In16_Cu, "Inner layer 16"  ) ,
                    ("CuIn17", PCB_LAYER_ID.In17_Cu, "Inner layer 17"  ) ,
                    ("CuIn18", PCB_LAYER_ID.In18_Cu, "Inner layer 18"  ) ,
                    ("CuIn19", PCB_LAYER_ID.In19_Cu, "Inner layer 19"  ) ,
                    ("CuIn20", PCB_LAYER_ID.In20_Cu, "Inner layer 20"  ) ,  
                    ("CuIn21", PCB_LAYER_ID.In21_Cu, "Inner layer 21"  ) ,
                    ("CuIn22", PCB_LAYER_ID.In22_Cu, "Inner layer 22"  ) ,
                    ("CuIn23", PCB_LAYER_ID.In23_Cu, "Inner layer 23"  ) ,
                    ("CuIn24", PCB_LAYER_ID.In24_Cu, "Inner layer 24"  ) ,
                    ("CuIn25", PCB_LAYER_ID.In25_Cu, "Inner layer 25"  ) ,
                    ("CuIn26", PCB_LAYER_ID.In26_Cu, "Inner layer 26"  ) ,
                    ("CuIn27", PCB_LAYER_ID.In27_Cu, "Inner layer 27"  ) ,
                    ("CuIn28", PCB_LAYER_ID.In28_Cu, "Inner layer 28"  ) ,
                    ("CuIn29", PCB_LAYER_ID.In29_Cu, "Inner layer 29"  ) ,
                    ("CuIn30", PCB_LAYER_ID.In30_Cu, "Inner layer 30"  )                                  
] 


class FabricationDataGenerator:
    def __init__(self, board):
        self.logger = logging.getLogger(__name__)
        self.board = board
        self.corrections = []
        self.path, self.filename = os.path.split(self.board.GetFileName())

    @property
    def nextpcb_root(self):
        nextpcb_path = os.path.join(self.path, "nextpcb")
        try:
            Path(nextpcb_path).mkdir(parents=True, exist_ok=True)
        except (PermissionError, OSError) as e:
            nextpcb_path = os.path.join(tempfile.gettempdir(), "nextpcb")
        return nextpcb_path

    @property
    def output_dir(self):
        return os.path.join(self.nextpcb_root, "output_files")

    def create_folders(self):
        """Create output folders if they not already exist."""
        # self.output_dir = os.path.join(self.nextpcb_root, "output_files")
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        self.gerberdir = os.path.join(self.nextpcb_root, "gerber")
        Path(self.gerberdir).mkdir(parents=True, exist_ok=True)

    def fill_zones(self):
        """Refill copper zones following user prompt."""
        # if self.parent.settings.get("gerber", {}).get("fill_zones", True):
        filler = ZONE_FILLER(self.board)
        zones = self.board.Zones()
        filler.Fill(zones)

    def get_position(self, footprint):
        """Calculate position based on center of bounding box"""
        if get_smd(footprint):
            return footprint.GetPosition()
        bbox = footprint.GetBoundingBox(False, False)
        return bbox.GetCenter()

    def generate_geber(self, layer_count=None):
        """Generating Gerber files"""
        # inspired by https://github.com/KiCad/kicad-source-mirror/blob/master/demos/python_scripts_examples/gen_gerber_and_drill_files_board.py
        pctl = PLOT_CONTROLLER(self.board)
        popt = pctl.GetPlotOptions()

        # https://github.com/KiCad/kicad-source-mirror/blob/master/pcbnew/pcb_plot_params.h
        popt.SetOutputDirectory(self.gerberdir)

        # Plot format to Gerber
        # https://github.com/KiCad/kicad-source-mirror/blob/master/include/plotter.h#L67-L78
        popt.SetFormat(1)

        # General Options
        popt.SetPlotValue(True)
        popt.SetPlotReference(True)
        popt.SetPlotInvisibleText(False)

        popt.SetSketchPadsOnFabLayers(False)

        # Gerber Options
        popt.SetUseGerberProtelExtensions(False)

        popt.SetCreateGerberJobFile(False)

        popt.SetSubtractMaskFromSilk(True)

        popt.SetPlotViaOnMaskLayer(False)  # Set this to True if you need untented vias

        popt.SetUseAuxOrigin(True)

        # Tented vias or not, selcted by user in settings
        popt.SetPlotViaOnMaskLayer(True)

        popt.SetUseGerberX2format(True)

        popt.SetIncludeGerberNetlistInfo(True)

        popt.SetDisableGerberMacros(False)

        if is_nightly(GetBuildVersion()):
            from pcbnew import DRILL_MARKS_NO_DRILL_SHAPE
            nites = DRILL_MARKS_NO_DRILL_SHAPE

            nitd =  popt.SetDrillMarksType(DRILL_MARKS_NO_DRILL_SHAPE)
        else:
            popt.SetDrillMarksType(PCB_PLOT_PARAMS.NO_DRILL_SHAPE)

        popt.SetPlotFrameRef(False)

        # delete all existing files in the output directory first
        for f in os.listdir(self.gerberdir):
            os.remove(os.path.join(self.gerberdir, f))

        # if no layer_count is given, get the layer count from the board
        if not layer_count:
            layer_count = self.board.GetCopperLayerCount()

        plot_plan_top = [
            ("CuTop", F_Cu, "Top layer"),
            ("SilkTop", F_SilkS, "Silk top"),
            ("MaskTop", F_Mask, "Mask top"),
            ("PasteTop", F_Paste, "Paste top"),
        ]
        plot_plan_bottom = [
            ("CuBottom", B_Cu, "Bottom layer"),
            ("SilkBottom", B_SilkS, "Silk top"),
            ("MaskBottom", B_Mask, "Mask bottom"),
            ("PasteBottom", B_Paste, "Paste bottom"),
            ("EdgeCuts", Edge_Cuts, "Edges"),
            ("VScore", Cmts_User, "V score cut"),
        ]

        plot_plan = []

        # Single sided PCB
        if layer_count == 1:
            plot_plan = plot_plan_top + plot_plan_bottom[-2:]
        # Double sided PCB
        elif layer_count == 2:
            plot_plan = plot_plan_top + plot_plan_bottom
        # Everything with inner layers
        else:
            # plot_plan = (
            #     plot_plan_top
            #     + [
            #         (f"CuIn{layer}", layer, f"Inner layer {layer}")
            #         for layer in range(1, layer_count - 1)
            #     ]
            #     + plot_plan_bottom
            # )
            plot_plan = (
                plot_plan_top 
                + [
                    plot_CuIn[layer - 1]
                    for layer in range(1, layer_count -1)
                    ] 

                +plot_plan_bottom
            )

        for layer_info in plot_plan:
            if layer_info[1] <= B_Cu:
                popt.SetSkipPlotNPTH_Pads(True)
            else:
                popt.SetSkipPlotNPTH_Pads(False)
            pctl.SetLayer(layer_info[1])
            pctl.OpenPlotfile(layer_info[0], PLOT_FORMAT_GERBER, layer_info[2])
            if pctl.PlotLayer() is False:
                self.logger.error(f"Error plotting {layer_info[2]}")
            self.logger.info(f"Successfully plotted {layer_info[2]}")
        pctl.ClosePlot()

    def generate_excellon(self):
        """Generate Excellon files."""
        drlwriter = EXCELLON_WRITER(self.board)
        mirror = False
        minimalHeader = False
        offset = self.board.GetDesignSettings().GetAuxOrigin()
        mergeNPTH = False
        drlwriter.SetOptions(mirror, minimalHeader, offset, mergeNPTH)
        drlwriter.SetFormat(False)
        genDrl = True
        genMap = True
        drlwriter.CreateDrillandMapFilesSet(self.gerberdir, genDrl, genMap)
        self.logger.info("Finished generating Excellon files")

    def zip_gerber_excellon(self):
        """Zip Gerber and Excellon files, ready for upload."""
        with ZipFile(self.zip_file_path, "w") as zipfile:
            for folderName, subfolders, filenames in os.walk(self.gerberdir):
                for filename in filenames:
                    if not filename.endswith(("gbr", "drl", "pdf")):
                        continue
                    filePath = os.path.join(folderName, filename)
                    zipfile.write(filePath, os.path.basename(filePath))
        self.logger.info("Finished generating ZIP file")

    def generate_cpl(self):
        """Generate placement file (CPL)."""
        cplname = f"CPL-{self.filename.split('.')[0]}.csv"
        # self.corrections = self.parent.library.get_all_correction_data()
        aux_orgin = self.board.GetDesignSettings().GetAuxOrigin()
        with open(
            os.path.join(self.output_dir, cplname), "w", newline="", encoding="utf-8"
        ) as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            writer.writerow(
                ["Designator", "Val", "Package", "Mid X", "Mid Y", "Rotation", "Layer"]
            )
            for part in self.parent.store.read_pos_parts():
                for fp in get_footprint_by_ref(self.board, part[0]):
                    if get_exclude_from_pos(fp):
                        continue
                    position = self.get_position(fp) - aux_orgin
                    writer.writerow(
                        [
                            part[0],
                            part[1],
                            part[2],
                            ToMM(position.x),
                            ToMM(position.y) * -1,
                            "",
                            "top" if fp.GetLayer() == 0 else "bottom",
                        ]
                    )
        self.logger.info("Finished generating CPL file")

    def generate_bom(self):
        """Generate BOM file."""
        bomname = f"BOM-{self.filename.split('.')[0]}.csv"
        with open(
            os.path.join(self.output_dir, bomname), "w", newline="", encoding="utf-8"
        ) as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            writer.writerow(["Value", "Designator", "Footprint", "MPN"])
            for part in self.parent.store.read_bom_parts():
                writer.writerow(part)
        self.logger.info("Finished generating BOM file")

    @property
    def zip_file_path(self):
        return os.path.join(
            self.output_dir, f"GERBER-{self.filename.split('.')[0]}.zip"
        )

    @contextlib.contextmanager
    def create_kicad_pcb_file(self):
        self.create_folders()
        self.fill_zones()
        self.generate_geber(None)
        self.generate_excellon()
        self.zip_gerber_excellon()
        yield self.zip_file_path
