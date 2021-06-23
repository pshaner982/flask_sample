#!/usr/bin/env python
# encoding: utf-8
"""
__init__.py
__init__.py

Created by Patrick Shaner 2021-06-17

Copyright (c) 2021 Patrick Shaner, All rights reserved
THE INFORMATION CONTAINED HEREIN IS PROPRIETARY AND CONFIDENTIAL

Entry point for initialization of flask sample

:Notes:
This is created for initial dev and testing.  Before production
service startup should be moved over to a factory method.


Version 2021-06-17:
    Initial creation
"""
from sample.utilities import StructLogs
log = StructLogs(module="sample.create_app")


def create_app(config_filename: str):
    from flask import Flask
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)

    from sample.model import db
    db.init_app(app)
    from sample.api import initialize_api_endpoints
    api = initialize_api_endpoints()
    api.init_app(app)

    log.info("================================================")
    log.info("\tSAMPLE APP")
    log.info("")

    for endpoint in app.url_map._rules:
        log.info(f"\tendpoint: {endpoint}")
    log.info("================================================")

    return app
