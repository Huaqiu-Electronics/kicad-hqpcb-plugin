from dataclasses import dataclass
import abc
import json


class PriceModelCol:
    DESC = 0
    VALUE = DESC + 1
    COL_COUNT = VALUE + 1


@dataclass
class PriceItem:
    id: str
    desc: str
    value: float
    parent: "PriceModelBase"


class PriceModelBase:
    @abc.abstractclassmethod
    def data(self, row: int, col: int):
        pass

    @abc.abstractclassmethod
    def name(self) -> "str":
        pass

    @abc.abstractclassmethod
    def sum(self):
        pass

    @abc.abstractclassmethod
    def get_items(self) -> "list[PriceItem]":
        pass

    @abc.abstractclassmethod
    def update(self, data: dict):
        pass

    def item_names(self):
        return []

    def clear(self):
        pass
