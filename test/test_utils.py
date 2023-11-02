#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import certifi
import ssl
ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())
class TestUtils:
    @staticmethod
    def read_json(fp: str):
        with open(fp, encoding="utf-8") as f:
            return json.load(f)
