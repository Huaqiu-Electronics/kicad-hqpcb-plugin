#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json


class TestUtils:
    @staticmethod
    def read_json(fp: str):
        with open(fp, encoding="utf-8") as f:
            return json.load(f)
