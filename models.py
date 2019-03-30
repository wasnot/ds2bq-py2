#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from google.appengine.ext import ndb


class User(ndb.Model):
    name = ndb.StringProperty()


class Item(ndb.Model):
    user = ndb.KeyProperty(kind=User)
    name = ndb.StringProperty()
