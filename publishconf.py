#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

SITEURL = 'http://datapfranc.github.io'
#RELATIVE_URLS = False

FEED_DOMAIN = SITEURL
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'

SOCIAL = SOCIAL + (('rss', SITEURL + '/' + FEED_ALL_ATOM),)

DELETE_OUTPUT_DIRECTORY = False

# Following items are often useful when publishing

# DISQUS_SITENAME = "datapfranc"
# DISQUS_SHORTNAME = "datapfranc"
# DISQUS_DISPLAY_COUNTS = True

GOOGLE_ANALYTICS = "UA-49087367-2"

# added to get my twitter timeline
TWITTER_USERNAME = 'dataPFranc'
TWITTER_WIDGET_ID = '738675033866940416'
