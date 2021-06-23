#!/usr/bin/env python
# encoding: utf-8
"""
room_request.py
sample/api/room_request.py

Created by Patrick Shaner 2021-06-17

Copyright (c) 2021 Patrick Shaner, All rights reserved
THE INFORMATION CONTAINED HEREIN IS PROPRIETARY AND CONFIDENTIAL

Collection of rest endpoint classes for updating and setting room sensors and
current occupancy.

Version 2021-06-17:
    Initial creation
"""
from flask import abort
from flask_restful import Resource
from flask_restful import fields
from flask_restful import marshal_with
from flask_restful import reqparse

from sample.model.model_orm import DeviceEvent
from sample.model.model_orm import Rooms
from sample.utilities import StructLogs

log = StructLogs(module="sample.rooms")

event_response = {
    "name": fields.String,
    "floor": fields.Integer,
    "uid": fields.String,
    "sensors": fields.String
}


class RoomSetup(Resource):

    _parser = reqparse.RequestParser()
    _room: Rooms = None
    _args: dict = None

    def __init__(self):
        self._parser.add_argument("name", type=str, help="Name of the room", location="json", required=True)
        self._parser.add_argument("company", type=str, help="Company name.", location="json", required=True)
        self._parser.add_argument("floor", type=int, default=1, help="Floor in building room is located",
                                  location="json")
        self._parser.add_argument("capacity", type=int, help="Max number of people allowed in space.",
                                  location="json")
        self._parser.add_argument("sensors", type=list, help="A list of sensors located in the room.",
                                  location="json")
        self._parser.add_argument("description", type=str, help="room description.")

    def get(self):
        """Gets the room with the matching name, company and floor returning the sensors attached to the room and
        current capacity as well.
        """
        try:
            self._log_request_type(verb="get")
            room = self._search_existing_room()
            record = {c: str(value) for c, value in room.__dict__.items() if not c.startswith("_")}
            if room:
                occupancy = DeviceEvent.get_rooms_current_occupancy(room.uid)
                record["occupancy"] = occupancy

            return record

        except Exception as e:
            log.error(e)

    @marshal_with(event_response)
    def post(self):
        """Post: Api request call
        Returns:
            the new room id, description and sensors attached to the room
        """
        try:
            self._log_request_type(verb="post")
            room = self._search_existing_room()
            if not room:
                self._create_new_room()
            else:
                self._room = room
                self._update_existing_room()
            log.info(f"Room sensors = {self._room.sensors}")
            return self._room

        except Exception as e:
            log.error(e)
            abort(400, f"Failed Post error {e}")

    def _search_existing_room(self) -> Rooms or None:
        """Searches the table rooms for a record with the name company and floor that matches args passed in.

        Returns:
            Rooms or None
        """
        return Rooms.search_room(name=self._args.get("name"), company=self._args.get("company"),
                                 floor=self._args.get("floor"))

    def _log_request_type(self, verb: str) -> None:
        """Logs the args and converts the request type
        Args:
            verb (str): API call
        Returns:
            None
        """
        self._args = self._parser.parse_args()
        log.info(f"{verb} room with {self._args}")

    def _create_new_room(self) -> None:
        """Leverages the request args to create a new room and locate the sensors attached
        to that room.  If sensors do not exist will create the devices as well.

        Then attaches the rooms and the sensors.

        Returns:
            None
        """
        log.info(f"Creating a new room from {self._args}")
        self._room = Rooms.create_room(**self._args)

    def _update_existing_room(self) -> None:
        """Leverages the request data to update an existing room.

        Returns:
            None
        """
        log.info(f"Updating room {self._room} with {self._args}")
        pass
