#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import webapp2

from views.bigquery_import import BigQueryImportHandler
from views.datastore_export import DatastoreExportHandler
from views.pubsub_receive import ReceivePubSubHandler

app = webapp2.WSGIApplication([
    ('/datastore-export', DatastoreExportHandler),
    ('/bigquery-import', BigQueryImportHandler),
    ('/_ah/push-handlers/receive', ReceivePubSubHandler),
], debug=True)
