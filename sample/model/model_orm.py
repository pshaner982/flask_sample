#!/usr/bin/env python
# encoding: utf-8
"""
model_orm.py
sample/model/model_orm.py

Created by Patrick Shaner 2021-06-17

Copyright (c) 2021 Patrick Shaner, All rights reserved
THE INFORMATION CONTAINED HEREIN IS PROPRIETARY AND CONFIDENTIAL

Database arch leveraging SQL Alchemy

Version 2021-06-17:
    Initial creation
"""
from datetime import datetime

from sample.model import db
from sqlalchemy import asc, desc
from sample.utilities import StructLogs

log = StructLogs(module="sample.models")


events_to_rooms = db.Table('events_for_room',
                           db.Column('room_uid', db.String, db.ForeignKey('rooms.uid')),
                           db.Column('event_id', db.Integer, db.ForeignKey("device_event.event_id")))


events_to_sensors = db.Table("events_for_sensor",
                             db.Column("dpu_id", db.Integer, db.ForeignKey('device.bpu_id')),
                             db.Column("event_id", db.Integer, db.ForeignKey("device_event.event_id")))


class Device(db.Model):
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    bpu_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    online = db.Column(db.Boolean, default=True)

    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    date_modified = db.Column(db.DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())

    room = db.Column(db.String, db.ForeignKey("rooms.uid"))
    events = db.relationship("DeviceEvent")

    def __repr__(self):
        return f"Device: {self.bpu_id}:{self.name}"

    @classmethod
    def search_device(cls, bpu_id: int):
        """Searches for an existing device record
        Args:
            bpu_id (int): device ID
        Returns:
            class
        """
        device = Device.query.filter_by(bpu_id=bpu_id).first()
        log.info(f"{device} found for {bpu_id}")
        return device

    @classmethod
    def create_device(cls, bpu_id: int, name: str = ""):
        """Searches if an existing device exist, will update the record.

        Args:
            bpu_id (int): unique id of the sensor
            name (str): User defined name for the sensor
        Returns:
            cls:  record for id.
        """
        device = Device.search_device(bpu_id=bpu_id)
        if device and name:
            device.name = name
        else:
            log.info(f"Creating {bpu_id} - {name}")
            device = Device()
            device.bpu_id = bpu_id
            device.name = name
            db.session.add(device)
        db.session.commit()
        return device


class Rooms(db.Model):
    """
    Notes:
        This might need to be enhanced to include address as part of the room if a company has multiple buildings.
    """
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    uid = db.Column(db.String(128), primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(256), nullable=True)
    floor = db.Column(db.Integer, default=1)
    max_capacity = db.Column(db.Integer, nullable=True)
    company = db.Column(db.String(), nullable=False)

    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    date_modified = db.Column(db.DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())

    sensors = db.relationship("Device")
    events = db.relationship("DeviceEvent")

    def __repr__(self):
        return f"{self.name} - {self.floor}: {self.sensors}"

    @classmethod
    def search_room(cls, name: str, company: str, floor=1):
        """Searches for an existing room record
        Args:
            name (str): device name
            company(str): company the account is set too.
            floor(int): the floor within a building the device is located, default=1
        Returns:
            class
        """
        uid = f"{name}{floor}{company}".lower()
        room = Rooms.query.filter_by(uid=uid).first()
        log.info(f"{room} found for {uid}")
        return room

    @classmethod
    def create_room(cls, **kwargs):
        """Leverages keyword args to create a new room.
        Keywords:
            name (str): user defined name for the room.
            company (str): Business name
            floor (int): floor the room is located within a building
            capacity (int): max capacity allowed for that space
            sensors (list): list of sensor details present in the room.
        Returns:
            record created.

        """
        name = kwargs.pop("name")
        company = kwargs.pop("company")
        floor = kwargs.pop("floor")
        sensors = kwargs.pop("sensors", [])
        uid = f"{name}{floor}{company}".lower()
        log.info(f"Creating a new room {uid}")
        room = Rooms()
        room.uid = uid
        room.name = name
        room.floor = floor
        room.company = company
        room.max_capacity = kwargs.get("capacity", None)

        for sensor in sensors:
            device = Device.create_device(sensor.get("dpu_id"), sensor.get("name"))
            if device:
                room.sensors.append(device)
        db.session.add(room)
        db.session.commit()
        return room

    def add_devices(self, sensor) -> None:
        self.sensors.append(sensor)

    def remove_all_devices(self) -> None:
        self.sensors = None
        db.session.commit()


class DeviceEvent(db.Model):
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    event_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime)
    direction = db.Column(db.Integer)
    room_occupancy = db.Column(db.Integer, nullable=False)
    room = db.Column(db.String, db.ForeignKey("rooms.uid"))
    sensor = db.Column(db.Integer, db.ForeignKey("device.bpu_id"))

    def __repr__(self):
        return f"[{self.event_id}-{self.timestamp}] {self.sensor} {self.room} -> {self.room_occupancy}"

    @classmethod
    def create_event(cls, **kwargs):
        """Creates a new event.
        Keywords:
            dpu_id (int): sensor device ID
            timestamp (str): Date time of the event
            direction (int): -1 departing the room, 1 entering the room
        Returns:
             None
        """
        try:
            log.info(f"Creating new event for {kwargs}")
            device = Device.search_device(kwargs.get("dpu_id"))
            date_format = datetime.strptime(kwargs.get("timestamp"), "%Y-%m-%dT%H:%M:%S.%fZ")
            new_occ = DeviceEvent.get_rooms_current_occupancy(device.room) + int(kwargs.get("direction"))
            event = DeviceEvent()
            event.room = device.room
            event.sensor = device.bpu_id
            event.direction = kwargs.get("direction")
            event.timestamp = date_format
            event.room_occupancy = new_occ
            db.session.add(event)
            db.session.commit()
            log.info(f"{event}")
            return event
        except Exception as e:
            log.exception(f"Error {e}")
            raise e

    @staticmethod
    def get_rooms_current_occupancy(room: str) -> int:
        """Searches the DeviceEvent table and gets the previous capacity
        Args:
            room (str): room id
        Returns:
            Int
        """
        occupancy = 0
        log.info(f"Room searching {room}")
        last_record = db.session.query(DeviceEvent).filter_by(room=room).order_by(desc(DeviceEvent.event_id)).first()
        if last_record:
            occupancy = last_record.room_occupancy
        else:
            log.warning(f"Room {room} has no previous events")
        if occupancy < 0:
            return 0
        else:
            return occupancy
