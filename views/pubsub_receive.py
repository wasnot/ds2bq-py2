#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging
import json

import webapp2


class ReceivePubSubHandler(webapp2.RequestHandler):
    """A handler for push subscription endpoint.."""

    def post(self):
        # Store the message in the datastore.
        logging.debug('Post body: {}'.format(self.request.body))
        # message = json.loads(urllib.unquote(self.request.body).rstrip('='))
        self.response.status = 200
