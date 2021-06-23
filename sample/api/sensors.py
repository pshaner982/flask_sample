#!/usr/bin/env python
# encoding: utf-8
"""
sensors.py
sample/api/sensors.py

Created by Patrick Shaner 2021-06-17

Copyright (c) 2021 Patrick Shaner, All rights reserved
THE INFORMATION CONTAINED HEREIN IS PROPRIETARY AND CONFIDENTIAL

Collection of API endpoint classes for processing sensor events.

Version 2021-06-17:
    Initial creation
"""
from flask_restful import Resource
from flask_restful import fields
from flask_restful import marshal_with
from flask_restful import reqparse

from sample.model.model_orm import Device
from sample.model.model_orm import DeviceEvent
from sample.utilities import StructLogs

log = StructLogs(module="sample.api.sensor")


batch_upload_fields_reference = {
    "file": fields.String
}


sensor_event_fields_reference = {
    "bpu_id": fields.Integer,
    "name": fields.String,
}

event_response = {
    "timestamp": fields.DateTime,
    "status": fields.Integer
}


class BatchSubmit(Resource):

    @marshal_with(batch_upload_fields_reference)
    def post(self) -> dict:
        """API endpoint to allow the services to batch upload csv file of messages

        Returns:
            json
        """
        # TODO add agrs supported by the api
        # TODO parse the args
        # TODO send file to back ground worker
        # TODO Send response
        pass


class SensorEvent(Resource):

    _parser = reqparse.RequestParser()
    _sensor: Device = None
    _args: dict = None

    def __init__(self):
        self._parser.add_argument("dpu_id", type=int, help="Device ID")
        self._parser.add_argument("timestamp", type=str, help="timestamp of event")
        self._parser.add_argument("direction", type=int, help="direction value, 1 for approaching, -1 for departing")

    def post(self):
        """Endpoint logic for a sensor to publish an event

        Returns:
            dict
        """
        try:
            self._args = self._parser.parse_args(strict=True)
            device = Device.search_device(self._args.get("dpu_id"))
            if device:
                event = DeviceEvent.create_event(**self._args)
        except Exception as e:
            return 400, {"code": 400, "message": f"Failed to process event because {e}"}

    def _look_up_sensor(self):
        """Looks up sensor record to create a back reference for the event

        :return:
        """
        device_id = self._args.get("dpu_id", None)
        log.info(f"Looking up device {device_id}")
        device = Device.query.filter_by(bpu_id=device_id).first()
        if not device:
            log.info(f"Need to create new device..")
        else:
            self._sensor = device
            log.info(f"Device located {self._sensor}")

    def _add_event_message(self) -> None:
        pass

class SensorLocation(Resource):

    @marshal_with(sensor_event_fields_reference)
    def get(self, device_id) -> tuple:
        """Endpoint logic for a sensor to publish an event

        Returns:
            dict
        """
        log.info(f"Deleting device id {device_id}")
        return Device.query.filter_by(bpu_id=device_id).first()

    def post(self, device_id) -> tuple:
        """Endpoint logic for a sensor to publish an event

        Returns:
            dict
        """
        log.info(f"Deleting device id {device_id}")
        return 400, {"status": "Not implemented"}

    def update(self, device_id) -> tuple:
        """Endpoint logic for a sensor to publish an event

        Returns:
            dict
        """
        log.info(f"Deleting device id {device_id}")
        return 400, {"status": "Not implemented"}

    def delete(self, device_id) -> tuple:
        """Endpoint logic for a sensor to publish an event

        Returns:
            dict
        """
        log.info(f"Deleting device id {device_id}")
        return 400, {"status": "Not implemented"}
