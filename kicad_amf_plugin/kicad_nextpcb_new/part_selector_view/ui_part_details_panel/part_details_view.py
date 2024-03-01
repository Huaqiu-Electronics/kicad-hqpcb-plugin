import wx
import wx.xrc
import wx.dataview
import requests
import webbrowser
import io
import json

from .ui_part_details_panel import UiPartDetailsPanel
import wx.dataview as dv


parameters = {
    "mpn": _("MPN"),
    "manufacturer": _("Manufacturer"),
    "package": _("Package / Footprint"),
    "category": _("Category"),
    "part_desc": _("Description"),
}
attribute_para = {
    "sku": _("SKU"),
    "vendor": _("Supplier"),
    "quantity": _("Stock"),
}


class PartDetailsView(UiPartDetailsPanel):
    def __init__(
        self,
        parent,
        id=wx.ID_ANY,
        pos=wx.DefaultPosition,
        size=wx.DefaultSize,
        style=wx.TAB_TRAVERSAL,
        name=wx.EmptyString,
    ):
        super().__init__(parent, id=id, pos=pos, size=size, style=style, name=name)

        # ---------------------------------------------------------------------
        # ----------------------- Properties List -----------------------------
        # ---------------------------------------------------------------------
        self.property = self.data_list.AppendTextColumn(
            _("Property"),
            width=180,
            mode=dv.DATAVIEW_CELL_ACTIVATABLE,
            align=wx.ALIGN_LEFT,
        )
        self.value = self.data_list.AppendTextColumn(
            _("Value"), width=-1, mode=dv.DATAVIEW_CELL_ACTIVATABLE, align=wx.ALIGN_LEFT
        )
        self.initialize_data()

    def initialize_data(self):
        # Initialize data and populate the data list
        self.data_list.DeleteAllItems()
        self.part_image.SetBitmap(wx.NullBitmap)

        for k, v in parameters.items():
            self.data_list.AppendItem([v, " "])
        for k, v in attribute_para.items():
            self.data_list.AppendItem([v, " "])
        self.data_list.AppendItem([_("Price"), " "])
        self.data_list.AppendItem([_("Datasheet"), " "])
        # update layout
        self.Layout()

    def on_open_pdf(self, e):
        """Open the linked datasheet PDF on button click."""
        item = self.data_list.GetSelection()
        row = self.data_list.ItemToRow(item)
        Datasheet = self.data_list.GetTextValue(row, 0)
        if self.pdfurl != "-" and Datasheet == "Datasheet":
            self.logger.info("opening %s", str(self.pdfurl))
            webbrowser.open("https:" + self.pdfurl)

    def get_scaled_bitmap(self, url):
        """Download a picture from a URL and convert it into a wx Bitmap"""
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.9999.999 Safari/537.36"
        }
        content = requests.get(url, headers=header).content
        io_bytes = io.BytesIO(content)
        image = wx.Image(io_bytes, type=wx.BITMAP_TYPE_ANY)
        result = wx.Bitmap(image)
        return result

    def get_part_data(self, clicked_part):
        """fetch part data from NextPCB API and parse it into the table, set picture and PDF link"""
        if clicked_part == "":
            self.report_part_data_fetch_error(
                _("returned data does not have expected clicked part")
            )
        self.info = clicked_part.get("part_info", {})
        self.supplier = clicked_part.get("supplier_chain", {})

        for i in range(self.data_list.GetItemCount()):
            self.data_list.DeleteItem(0)
        for k, v in parameters.items():
            val = self.info.get(k, "-")
            if val != "null" and val:
                self.data_list.AppendItem([v, str(val)])
            else:
                self.data_list.AppendItem([v, "-"])

        if self.supplier != []:
            for k, v in attribute_para.items():
                val = self.supplier.get(k, "-")
                if val != "null" and val:
                    self.data_list.AppendItem([v, str(val)])
                else:
                    self.data_list.AppendItem([v, "-"])
            prices_stair = self.supplier.get("price", [])
            if prices_stair == None:
                self.data_list.AppendItem(["Price", "-"])
            else:
                price_echelon = {}
                # Populate price_echelon based on prices_stair data
                for index, price_range in enumerate(prices_stair):
                    break_min = price_range.get("breakMin")
                    break_max = price_range.get("breakMax")
                    if break_max is None:
                        key = f">{break_min} Piece(￥)"
                    else:
                        key = f"{break_min}-{break_max} Piece(￥)"
                    price_echelon[key] = price_range["rmb"]
                # Populate self.data_list with the key-value pairs
                for key, value in price_echelon.items():
                    self.data_list.AppendItem([key, str(value)])

        self.pdfurl = self.info.get("datasheet", {})
        self.pdfurl = "-" if self.pdfurl == "" else self.pdfurl
        self.data_list.AppendItem(
            [
                _("Datasheet"),
                self.pdfurl,
            ]
        )
        self.data_list.Bind(wx.dataview.EVT_DATAVIEW_ITEM_ACTIVATED, self.on_open_pdf)
        picture = self.info.get("image", [])
        if picture:
            self.part_image.SetBitmap(
                self.get_scaled_bitmap(
                    picture,
                )
            )
        else:
            self.part_image.SetBitmap(wx.NullBitmap)
        self.Layout()

    def report_part_data_fetch_error(self, reason):
        wx.MessageBox(
            _(f"Failed to download part detail: ({reason})\r\n"),
            _(f"We looked for a part named:\r\n{self.info.find('mpn')}\r\n[hint: did you fill in the NextPCB field correctly?]"),
            _("Error"),
            style=wx.ICON_ERROR,
        )
        self.Destroy()
