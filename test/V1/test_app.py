#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
sys.path.append('../src/V1/')

import os
import tempfile

import pytest
import v1


@pytest.fixture
def client():
    v1.app.config['TESTING'] = True
    client = v1.app.test_client()

    yield client

def test_status(client):
    rv = client.get('/servicio/v1/status')
    json_data = rv.get_json()
    assert json_data['status']=="OK" and rv.status_code == 200