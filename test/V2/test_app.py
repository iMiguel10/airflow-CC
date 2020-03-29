#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
sys.path.append('../src/V2/')

import os
import tempfile

import pytest
import v2


@pytest.fixture
def client():
    v2.app.config['TESTING'] = True
    client = v2.app.test_client()

    yield client

def test_status(client):
    rv = client.get('/servicio/v2/status')
    json_data = rv.get_json()
    assert json_data['status']=="OK" and rv.status_code == 200