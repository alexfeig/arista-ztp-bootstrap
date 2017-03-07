#!/usr/bin/env python

"""bootstrap.py - a script that runs on an Arista switch that is ZTP booting

   This script:

   * Gets the MAC address of the management interface (Ma1)
   * Queries NetBox (https://github.com/digitalocean/netbox) for the device name and IP address
   * Sets the device IP, hostname, and initial username and password
   * Calls to Jenkins to kick off job - in this case an Ansible playbook that configures the switch
      o Jenkins token is configured when enabling "Trigger builds remotely (e.g., from scripts)" on a job

   Note: This script will sleep for 600 seconds to allow for Ansible to complete. The reload is handled through
         Ansible, and not this script.
"""

import base64
import urllib2
import json
import time
from subprocess import call


# Variables - set as required

device_password = 'arista'  # Note: Leave this password unencrypted.
ipam_url = 'http://ipam.home.lab/api/dcim/devices/?mac_address='
jenkins_username = 'admin'
jenkins_password = 'arista'
jenkins_base_url = 'http://172.16.50.5:8080/job/'
jenkins_project = 'Ansible-Test'
jenkins_token = 'foo'
dns_server = '172.16.50.1'

# Script

def get_mac():
    f = open('/sys/class/net/ma1/address', 'r')
    mac = f.read()
    f.close()

    return mac


def get_facts(url_assembled):
    response = urllib2.urlopen(url_assembled)
    jsonresponse = json.load(response)
    device_name = jsonresponse[0]['name']
    device_ip = jsonresponse[0]['primary_ip']['address']

    return {'device_name': device_name, 'device_ip': device_ip}


def set_config(device_name, device_ip):
    config = ""
    config = config + "enable\n"
    config = config + "configure replace clean-config\n"
    config = config + "configure\n"
    config = config + "hostname " + device_name + "\n"
    config = config + "ip name-server vrf default " + dns_server + "\n"
    config = config + "interface Management1\n"
    config = config + "ip address " + device_ip + "\n"
    config = config + "username admin privilege 15 secret " + device_password

    call("echo \"" + config + "\" | " + "/usr/bin/FastCli", shell=True)


# Borrowed from https://github.com/pycontribs/jenkinsapi/issues/19#issuecomment-18880801
def auth_headers(username, password):
    return 'Basic ' + base64.encodestring('%s:%s' % (username, password))[:-1]


# Borrowed and altered from https://github.com/pycontribs/jenkinsapi/issues/19#issuecomment-18880801
def get_jenkins():
    auth = auth_headers(jenkins_username, jenkins_password)
    a_url = jenkins_base_url + jenkins_project + "/build?token=" + jenkins_token
    req = urllib2.Request(a_url)
    req.add_header('Authorization', auth)

    print urllib2.urlopen(req).read()


def main():
    mac_address = get_mac()
    url_assembled = ipam_url + mac_address
    switch_facts = get_facts(url_assembled)
    set_config(**switch_facts)
    get_jenkins()
    time.sleep(600)  # We sleep until Ansible finishes writing the config, then the switch will automagically reboot.


if __name__ == "__main__":
    main()
