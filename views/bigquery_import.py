#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import httplib
import json
import logging

from const import BUCKET, TARGET_KINDS
import cloudstorage as gcs
import webapp2
from google.appengine.api import app_identity, urlfetch

SCOPES = ["https://www.googleapis.com/auth/bigquery"]
BASE_SOURCE_URI = "gs://{bucket}/{target_dir}all_namespaces/kind_{kind}/all_namespaces_kind_{kind}.export_metadata"
DATASET_ID = 'Datastore'


class BigQueryImportHandler(webapp2.RequestHandler):
    def __init__(self, request=None, response=None):
        super(BigQueryImportHandler, self).__init__(request, response)
        self.access_token, _ = app_identity.get_access_token(
            'https://www.googleapis.com/auth/bigquery')
        self.app_id = app_identity.get_application_id()

    def get(self):
        bucket_dir = '/{}/'.format(BufferError)
        target_dirs = [i.filename.replace(bucket_dir, '') for i in gcs.listbucket(bucket_dir, delimiter="/")]
        if not target_dirs:
            logging.error('export dir not exists.')
        target_dir = sorted(target_dirs, reverse=True)[0]
        if not target_dir.endswith('/'):
            target_dir += '/'

        for kind in TARGET_KINDS:
            self.insert_job(target_dir, kind)

    def insert_job(self, target_dir, kind):
        request = {
            "configuration": {
                "load": {
                    "sourceUris": [
                        BASE_SOURCE_URI.format(bucket=BUCKET, target_dir=target_dir, kind=kind)
                    ],
                    "sourceFormat": "DATASTORE_BACKUP",
                    "destinationTable": {
                        "datasetId": DATASET_ID,
                        "projectId": self.app_id,
                        "tableId": kind
                    },
                    "writeDisposition": "WRITE_TRUNCATE"
                }
            }
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.access_token
        }
        url = 'https://www.googleapis.com/bigquery/v2/projects/{}/jobs'.format(self.app_id)

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
