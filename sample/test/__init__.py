#!/usr/bin/env python
# encoding: utf-8
"""
__init__.py
sample/test/__init__.py

Created by Patrick Shaner 2021-06-17

Copyright (c) 2021 Patrick Shaner, All rights reserved
THE INFORMATION CONTAINED HEREIN IS PROPRIETARY AND CONFIDENTIAL

Utilities and fixtures for testing.

Version 2021-06-17:
    Initial creation
"""
import csv
import os

import pytest

from sample import create_app

BASE = os.path.dirname(os.path.abspath(__file__))


def create_event_messages():
    event_samples = os.path.join(BASE, "samples", "dpu_data.csv")

    with open(event_samples, "r") as f_in:
        data = csv.DictReader(f_in)
        return [x for x in data]


def create_default_room_and_sensors():
    message_body = {
        "name": "SpaceA",
        "description": "Space A",
        "capacity": 10,
        "company": "Density",
        "floor": 1,
        "sensors": [
            {"dpu_id": 423, "name": "Doorway Z"},
            {"dpu_id": 283, "name": "Doorway Y"}
        ]
    }
    return message_body


@pytest.fixture(scope="module")
def client():
    from sample.model import db
    app = create_app("config.py")
    # app.config['TESTING'] = True
    with app.app_context():
        db.drop_all()
        db.create_all()
        with app.test_client() as client:
            yield client
