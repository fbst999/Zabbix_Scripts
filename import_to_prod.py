#Import Zabbix XML templates

from pyzabbix.api import ZabbixAPI, ZabbixAPIException
import os
import sys   
import glob

path = '/opt/zabbix/template_exported_to_production'

# The hostname at which the Zabbix web interface is available
zabbix_url = 'http://zabbix.local/zabbix/'
zabbix_user="Zabbix_API"
zabbix_password="password"

zapi = ZabbixAPI(zabbix_url,user=zabbix_user,password=zabbix_password)

# Login to the Zabbix API

rules = {
    'applications': {
        'createMissing': True,
    },
    'discoveryRules': {
        'createMissing': True,
        'updateExisting': True
    },
    'graphs': {
        'createMissing': True,
        'updateExisting': True
    },
    'groups': {
        'createMissing': True
    },
    'hosts': {
        'createMissing': True,
        'updateExisting': True
    },
    'images': {
        'createMissing': True,
        'updateExisting': True
    },
    'items': {
        'createMissing': True,
        'updateExisting': True
    },
    'maps': {
        'createMissing': True,
        'updateExisting': True
    },
    'screens': {
        'createMissing': True,
        'updateExisting': True
    },
    'templateLinkage': {
        'createMissing': True,
    },
    'templates': {
        'createMissing': True,
        'updateExisting': True
    },
    'templateScreens': {
        'createMissing': True,
        'updateExisting': True
    },
    'triggers': {
        'createMissing': True,
        'updateExisting': True
    },
    'valueMaps': {
        'createMissing': True,
        'updateExisting': True
    },
}

if os.path.isdir(path):
    #path = path/*.xml
    files = glob.glob(path+'/*.xml')
    for file in files:
        print(file)
        with open(file, 'r') as f:
            template = f.read()
            try:
                #zapi.confimport('xml', template, rules)
                zapi.configuration.import('xml',template,rules)
            except ZabbixAPIException as e:
                print(e)
        print('')
elif os.path.isfile(path):
    files = glob.glob(path)
    for file in files:
        with open(file, 'r') as f:
            template = f.read()
            try:
                zapi.configuration.import('xml',template,rules)
            except ZabbixAPIException as e:
                print(e)
else:
    print('Need a xml file')
