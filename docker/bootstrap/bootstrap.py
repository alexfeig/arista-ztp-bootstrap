#!/usr/bin/env python

import urllib2
import json
from subprocess import call

f = open('/sys/class/net/ma1/address','r')
mac = f.read()

url = 'http://ipam.home.lab/api/dcim/devices/?mac_address='

url_assembled = url + mac

f.close()

response = urllib2.urlopen(url_assembled)
jsonresponse = json.load(response)

device_name = jsonresponse[0]['name']
device_ip = jsonresponse[0]['primary_ip']['address']

config = ""
config = config + "enable\n"
config = config + "configure\n"
config = config + "hostname " + device_name
config = config + "\ninterface Management1\n"
config = config + "ip address " + device_ip

call("echo \"" + config + "\" | " + "/usr/bin/FastCli",shell=True)