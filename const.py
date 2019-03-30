#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os

from models import User, Item

BUCKET = os.getenv('TARGET_BUCKET_NAME')
PREFIX = os.getenv('BACKUP_PREFIX', '')
TARGET_KINDS = [User.__name__, Item.__name__]
