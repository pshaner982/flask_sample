#!/usr/bin/env python
# encoding: utf-8
"""
status.py
sample/api/status.py

Created by Patrick Shaner 2021-06-17

Copyright (c) 2021 Patrick Shaner, All rights reserved
THE INFORMATION CONTAINED HEREIN IS PROPRIETARY AND CONFIDENTIAL

API status and health collection.

Version 2021-06-17:
    Initial creation
"""
from flask_restful import Resource

from sample.utilities import StructLogs

log = StructLogs(module="sample.apl.status")


class HealthCheck(Resource):

    def get(self) -> tuple:
        log.info(f"Health check, system is running and will return 200")
        return {"status": "running"}, 200
