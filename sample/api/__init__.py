#!/usr/bin/env python
# encoding: utf-8
"""
__init__.py
sample/api/__init__.py

Created by Patrick Shaner 2021-06-17

Copyright (c) 2021 Patrick Shaner, All rights reserved
THE INFORMATION CONTAINED HEREIN IS PROPRIETARY AND CONFIDENTIAL

Initialize API endpoints

Version 2021-06-17:
    Initial creation
"""

from flask_restful import Api

from sample.api.sensors import BatchSubmit
from sample.api.sensors import SensorEvent
from sample.api.sensors import SensorLocation
from sample.api.status import HealthCheck
from sample.utilities import StructLogs
from sample.api.room_request import RoomSetup


log = StructLogs(module="sample.init")


def initialize_api_endpoints():
    log.info("Initializing API endpoints")
    _api = Api()
    _api.add_resource(HealthCheck, "/", "/health")
    _api.add_resource(SensorEvent, "/event")
    _api.add_resource(RoomSetup, "/room")

    # TODO not implemented
    _api.add_resource(SensorLocation, "/sensor/<device_id>")
    _api.add_resource(BatchSubmit, '/sensor/batch_upload')

    return _api
