#!/usr/bin/env python
# encoding: utf-8
"""
app.py

Created by Patrick Shaner 2021-06-17

Copyright (c) 2021 Patrick Shaner, All rights reserved
THE INFORMATION CONTAINED HEREIN IS PROPRIETARY AND CONFIDENTIAL

Entry point for initialization of flask sample


Version 2021-06-17:
    Initial creation
"""

from sample import create_app
from sample.utilities import StructLogs
log = StructLogs(module="app.start")

app = create_app('config.py')


def create_sample_device():
    from sample.model import db
    from sample.model.model_orm import Device
    test_device = Device()
    test_device.bpu_id = 423
    test_device.name = "test_423"
    test_device.online = True
    # test_device.rooms =
    db.session.add(test_device)
    db.session.commit()
    log.info(f"Created company test device {test_device.bpu_id}")


def create_sample_rooms():
    from sample.model import db
    from sample.model.model_orm import Rooms
    for _ in range(2):
        room = Rooms()
        room.floor = 1
        db.session.add(room)
        db.session.commit()


# def create_sample_company():
#     from sample.model import db
#     from sample.model.model_orm import Account
#     test_device = Account()
#     test_device.name = "Test Name"
#     test_device.address_street_1 = "123 Main Street"
#     test_device.address_country = "US"
#     test_device.address_state = "CA"
#     test_device.address_zip = 99906
#     db.session.add(test_device)
#     db.session.commit()
#     log.info(f"Created company test name {test_device.uid}")


@app.cli.command()
def createdb():
    from sample.model import db
    from sample.model.model_orm import DeviceEvent, Rooms, Device
    engine = db.engine
    db.create_all()
    # create_sample_device()
    # create_sample_rooms()
    # create_sample_company()


@app.cli.command()
def dropdb():
    from sample.model import db
    db.drop_all()
