#!/usr/bin/python
import datetime
import os
import subprocess
from optparse import OptionParser
import hashlib

# app configuration
APP_ROOT = os.path.dirname(os.path.realpath(__file__))
MEDIA_ROOT = os.path.join(APP_ROOT, 'static')
MEDIA_URL = '/static/'
PHANTOM = '/usr/local/bin/phantomjs'
SCRIPT = os.path.join(APP_ROOT, 'screenshot.js')

parser = OptionParser()
parser.add_option("-u", "--url", dest="url", help="url to get a snapshot of")
(options, args)=parser.parse_args()

if options.url != None:
        url = str(options.url)
else:   
        url = "http://www.hp.com"
print "getting snapshot of " + url

filename = "bookmarks-" + (hashlib.md5(url).hexdigest()) + ".png" 
outfile = os.path.join(MEDIA_ROOT, filename)
params = [PHANTOM, SCRIPT, url, outfile]

exitcode = subprocess.call(params)
