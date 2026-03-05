#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

class Config(object):
    # ✅ Fixed: Hardcoded credentials hata diye — env vars se lo
    BOT_TOKEN  = os.environ.get("BOT_TOKEN", "")
    API_ID     = int(os.environ.get("API_ID", "0"))
    API_HASH   = os.environ.get("API_HASH", "")
    AUTH_USERS = os.environ.get("AUTH_USERS", "")
