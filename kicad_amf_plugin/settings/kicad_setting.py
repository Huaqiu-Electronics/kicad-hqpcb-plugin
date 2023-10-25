import json

import wx
import os
import logging


class KiCadSetting:
    def read_lang_setting():
        try:
            import pcbnew

            kicad_setting_path = str(pcbnew.SETTINGS_MANAGER.GetUserSettingsPath())
            logging.info(f"Kicad setting path {kicad_setting_path}")
            print(f"Kicad setting path {kicad_setting_path}")
            if len(kicad_setting_path):
                kicad_common_json = os.path.join(
                    kicad_setting_path, "kicad_common.json"
                )
                with open(kicad_common_json) as f:
                    data = json.loads(f.read())
                    lang: str = data["system"]["language"]
                    if lang.count("中文"):
                        return wx.LANGUAGE_CHINESE_SIMPLIFIED
                    elif lang.count("日本"):
                        return wx.LANGUAGE_JAPANESE_JAPAN
            else:
                logging.error("Empty KiCad config path!")
        except:
            logging.error("Cannot read the language setting of KiCad!")
        return wx.LANGUAGE_ENGLISH
