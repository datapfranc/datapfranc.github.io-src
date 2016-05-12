#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from __future__ import unicode_literals
import platform

def is_windows():
    if platform.system() == 'Windows': return True
    else: return False

def system_path(path):
    """Return path with forward or backwards slashes as necessary based on OS"""
    if is_windows(): return path.replace('/', '\\')
    else: return path.replace('\\', '/')

######################## MO Notes on blog settings #############################



########################### General Settings ###################################

AUTHOR = u'Martin Ouellet'
SITENAME = u'DataPlatform Franchising'
SITESUBTITLE = u"A site dedicated to experimenting DataPlatform Franchising concept"
SITEURL = ''

PATH = 'content'
DELETE_OUTPUT_DIRECTORY = False

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = u'en'
USE_FOLDER_AS_CATEGORY = False
DISPLAY_CATEGORIES_ON_MENU = False
DEFAULT_DATE_FORMAT = '%a %d %B %Y'

# when blog has no Date, it will use mdate from file
DEFAULT_DATE = 'fs'
# to control whether all files under /pages are diplayed under primary menu (default is True)
DISPLAY_PAGES_ON_MENU = True

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS = (
         ('DBMS2', 'http://www.dbms2.com/'),
         ('Librarything', 'http://librarything.com/'),
         ('Goodreads', 'https://www.goodreads.com/'),
         ('Babelio', 'https://babelio.com/'),
         ('Paul Miller blog', 'http://cloudofdata.com/blog/'),
        )

# Social widget
SOCIAL = (('github', 'http://github.com/mart2010'),
          ('linkedin', 'http://linkedin.com/in/martinouellet'),
          ('Personal blog', 'http://martin-ouellet.blogspot.ch/'),
         )

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

ARTICLE_URL = '{category}/{slug}/'
ARTICLE_SAVE_AS = '{category}/{slug}/index.html'
# use basename to sort articles by filename (default 'reversed-date', sort articles by date in reverse)
ARTICLE_ORDER_BY = 'basename'

PAGE_URL = '{slug}.html'
PAGE_SAVE_AS = '{slug}.html'
TAG_URL = 'tags/{slug}.html'
TAG_SAVE_AS = 'tags/{slug}.html'
TAGS_URL = 'tags.html'

# Generate archive
YEAR_ARCHIVE_SAVE_AS = 'posts/{date:%Y}/index.html'

################## Add custom css #########################
CUSTOM_CSS = 'static/custom.css'
# all dirs to be included in the generated output
STATIC_PATHS = ['images', 'extra/custom.css', 'extra/href_scroll.js', 'extra/jquery.zoom.js']
EXTRA_PATH_METADATA = {'extra/custom.css':{'path':'static/custom.css'},
                    'extra/href_scroll.js':{'path':'theme/js/href_scroll.js'},
                    'extra/jquery.zoom.js':{'path':'theme/js/jquery.zoom.js'},
                       }
for k in EXTRA_PATH_METADATA.keys(): # Fix backslash paths to resources if on Windows
    EXTRA_PATH_METADATA[system_path(k)] = EXTRA_PATH_METADATA.pop(k)


##################### Exterior Services ############################
# DISQUS_SITENAME = 'datapfran.githib.com'
# DISQUS_SHORTNAME = 'datapfran'
# DISQUS_DISPLAY_COUNTS = True

GOOGLE_ANALYTICS = "UA-49087367-2"

# after creating my Addthis account (using gmail main ..)
ADDTHIS_PROFILE = 'ra-572cd8ecd555b197'
ADDTHIS_DATA_TRACK_ADDRESSBAR = False



####################### Theme-Specific Settings #########################
THEME = 'themes/pelican-bootstrap3'#'html5-dopetrope'

# Pelican Theme-Specific Variables
BOOTSTRAP_THEME =  'cosmo' # 'simplex' #'sandstone' #'lumen'

SITELOGO = 'images/logo.png'
SITELOGO_SIZE = 36
FAVICON = 'images/favicon.png'

ABOUT_ME = "I'm a business intelligence architect by choice. I enjoy doing backend stuff and data-oriented projects.\
<p>Find out more about me at <strong><a href=\"http://martin-ouellet.blogspot.ch\" title=\"Personal Archive\">martin-ouellet</a></strong></p>\
<p>You can also contact me " + "<a href='mailto:mart2010.l@gmail.com?subject=dataPFranc-feedback'>here</a>"
AVATAR = "/images/headshot.png"

# dont use banner
# BANNER = "/images/banner.png"

DISPLAY_ARTICLE_INFO_ON_INDEX = True
DISPLAY_RECENT_POSTS_ON_SIDEBAR = True
SHOW_ARTICLE_CATEGORY = False

# tags cloud stuff
DISPLAY_TAGS_ON_SIDEBAR = True
DISPLAY_TAGS_INLINE = True

TAG_CLOUD_MAX_ITEMS = 8
DISPLAY_TAGS_INLINE = True
TAG_CLOUD_STEPS = 4
TAG_CLOUD_SORTING = 'alphabetically'

PYGMENTS_STYLE = 'monokai'

############################ Plugins ######################################
PLUGIN_PATHS = ['plugins']
PLUGINS = ['simple_footnotes', 'extract_toc', 'feed_summary', 'tag_cloud']
# add 'tag_cloud' if using the full tag stuff: https://github.com/getpelican/pelican-plugins/tree/master/tag_cloud
FEED_USE_SUMMARY = True
SUMMARY_MAX_LENGTH = 100

MD_EXTENSIONS = ['toc', 'fenced_code', 'codehilite(css_class=highlight)', 'extra']
#MD_EXTENSIONS = ['codehilite(css_class=highlight)', 'extra']
