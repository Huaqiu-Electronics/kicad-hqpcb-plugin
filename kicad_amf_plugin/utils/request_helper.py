from urllib import parse


class RequestHelper:
    @staticmethod
    def convert_dict_to_request_data(input: "dict"):
        return parse.urlencode(list(input.items())).encode()
