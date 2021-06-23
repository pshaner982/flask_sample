#!/usr/bin/env python
# encoding: utf-8
"""
test_load_data.py
sample/test/test_load_data.py

Created by Patrick Shaner 2021-06-17

Copyright (c) 2021 Patrick Shaner, All rights reserved
THE INFORMATION CONTAINED HEREIN IS PROPRIETARY AND CONFIDENTIAL

Unit test to load the database with test data

Version 2021-06-17:
    Initial creation
"""
import json

import pytest

from sample.test import client
from sample.test import create_default_room_and_sensors
from sample.test import create_event_messages

EVENT_SAMPLES = create_event_messages()


def test_health(client):
    health = client.get("/health")
    root = client.get("/")
    assert health.status == root.status
    assert health.status == "200 OK"


def test_event_message():
    assert EVENT_SAMPLES is not None
    assert len(EVENT_SAMPLES) > 1
    assert isinstance(EVENT_SAMPLES, list) is True


def test_load_room(client):
    response = client.post("/room", data=json.dumps(create_default_room_and_sensors()),
                           content_type='application/json')
    data = response.json
    assert response._status_code == 200
    assert data.get("name", None) is not None
    assert data.get("uid", None) is not None


@pytest.mark.parametrize("message", EVENT_SAMPLES)
def test_event_processing(client, message):
    print(json.dumps(message))
    response = client.post("/event", data=json.dumps(message), content_type='application/json')
    assert response._status_code == 200


def test_get_room(client):
    request = client.get("/room", data=json.dumps(create_default_room_and_sensors()), content_type='application/json')
    data = request.json
    assert request._status_code == 200
    assert data.get("occupancy", None) is not None

    assert data.get("occupancy", None) is not None
