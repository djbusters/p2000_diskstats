#!/usr/bin/env python

import getpass
import hashlib
import requests
from urllib2 import Request, urlopen, URLError
from lxml import etree as ET
import sys

host = raw_input('IP or Hostname: ')
username = raw_input('Username: ')
password = getpass.getpass('Pass: ')

md5_data = username + '_' + password
md5_hex = hashlib.md5(md5_data).hexdigest()

url = "http://%s/api/login/" % host + md5_hex

request = Request(url)

response = urlopen(request).read()
answerxml = ET.fromstring(response)

for property in answerxml.xpath('//PROPERTY'):
    for attrib in property.attrib:
        if property.attrib[attrib] == 'response':
            if property.text == 'Authentication Unsuccessful':
                print 'Authentication Unsuccessful'
                sys.exit()
            else:
                sessionkey =  property.text

disk_url = "http://%s/api/show/disks" % host
disk_req = Request(disk_url, headers={ 'sessionKey': sessionkey })
disks = urlopen(disk_req).read()
disksxml = ET.fromstring(disks)

for property in disksxml.xpath('//PROPERTY'):
    for attrib in property.attrib:
        if property.attrib[attrib] =='durable-id':
            print property.text,
        if property.attrib[attrib] =='serial-number':
            print property.text,
        if property.attrib[attrib] =='status':
            print property.text
