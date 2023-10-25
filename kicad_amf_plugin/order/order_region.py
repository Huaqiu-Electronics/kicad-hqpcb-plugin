from enum import Enum
from .supported_region import SupportedRegion


class URL_KIND(Enum):
    QUERY_PRICE = 0
    PLACE_ORDER = 1


class OrderRegion:
    AVAILABLE_URLS = {
        SupportedRegion.CHINA_MAINLAND: {
            URL_KIND.PLACE_ORDER: "https://www.hqpcb.com/External/fileQuote",
            URL_KIND.QUERY_PRICE: "https://www.hqpcb.com/public/ajax_valuation",
        },
        SupportedRegion.EUROPE_USA: {
            URL_KIND.PLACE_ORDER: "https://www.nextpcb.com/Upfile/kiCadUpFile",
            URL_KIND.QUERY_PRICE: "https://www.nextpcb.com/ajax/valuation",
        },
        SupportedRegion.JAPAN: {
            URL_KIND.PLACE_ORDER: "https://jp.nextpcb.com/Upfile/kiCadUpFile",
            URL_KIND.QUERY_PRICE: "https://jp.nextpcb.com/ajax/valuation",
        },
    }

    @staticmethod
    def get_url(region: SupportedRegion, kind: URL_KIND):
        if region in OrderRegion.AVAILABLE_URLS:
            return OrderRegion.AVAILABLE_URLS[region][kind]
