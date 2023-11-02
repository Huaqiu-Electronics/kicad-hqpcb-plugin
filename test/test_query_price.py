from .test_utils import TestUtils
from . import TEST_ROOT
from kicad_amf_plugin.utils.request_helper import RequestHelper
from kicad_amf_plugin.order.supported_region import SupportedRegion
from kicad_amf_plugin.order.order_region import OrderRegion, URL_KIND

import urllib
import os
import json

REQUESTS = {
    SupportedRegion.CHINA_MAINLAND: "hq_pcb.json",
    SupportedRegion.JAPAN: "next_pcb_jp.json",
    SupportedRegion.EUROPE_USA: "next_pcb_en.json",
}


def test_query_price():
    for i in REQUESTS:
        form = TestUtils.read_json(os.path.join(TEST_ROOT, "query_price", REQUESTS[i]))
        rep = urllib.request.Request(
            OrderRegion.get_url(i, URL_KIND.QUERY_PRICE),
            data=RequestHelper.convert_dict_to_request_data(form),
        )
        fp = urllib.request.urlopen(rep)
        data = fp.read()
        encoding = fp.info().get_content_charset("utf-8")
        content = data.decode(encoding)
        quote = json.loads(content)
        if "code" in quote:
            assert quote["code"] == 200
        else:
            assert quote["total"] > 0
