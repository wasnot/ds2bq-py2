#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import datetime
import httplib
import json
import logging

import webapp2
from google.appengine.api import app_identity
from google.appengine.api import urlfetch

from const import BUCKET, PREFIX, TARGET_KINDS


class DatastoreExportHandler(webapp2.RequestHandler):
    def get(self):
        access_token, _ = app_identity.get_access_token(
            'https://www.googleapis.com/auth/datastore')
        app_id = app_identity.get_application_id()
        timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%S')

        # Bucket name must starts with 'gs://' keyword.
        output_url_prefix = 'gs://{}/{}'.format(BUCKET, PREFIX)
        if not output_url_prefix.endswith('/'):
            output_url_prefix += '/'
        output_url_prefix += timestamp

        # 保存するentityの条件をrequest bodyに含めます。
        # 今回はAppEngineアプリ内のModel定義からkind名を取得しています。
        entity_filter = {
            'kinds': TARGET_KINDS,
            'namespace_ids': []
        }
        # Below is same as the tutorial.
        request = {
            'project_id': app_id,
            'output_url_prefix': output_url_prefix,
            'entity_filter': entity_filter
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + access_token
        }
        url = 'https://datastore.googleapis.com/v1beta1/projects/{}:export'.format(app_id)
        try:
            result = urlfetch.fetch(
                url=url,
                payload=json.dumps(request),
                method=urlfetch.POST,
                deadline=60,
                headers=headers)
            if result.status_code == httplib.OK:
                logging.info(result.content)
            elif result.status_code >= 500:
                logging.error(result.content)
            else:
                logging.warning(result.content)
            self.response.status_int = result.status_code
        except urlfetch.Error:
            logging.exception('Failed to initiate export.')
            self.response.status_int = httplib.INTERNAL_SERVER_ERROR
