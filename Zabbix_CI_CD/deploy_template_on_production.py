#from pyzabbix.api import ZabbixAPI, ZabbixAPIException
import glob
import requests
import json

ZABBIX_API_URL = "http://zbxurl.local/zabbix/api_jsonrpc.php"
UNAME = "Zabbix"
PWORD = "password"

r = requests.post(ZABBIX_API_URL,
                  json={
                      "jsonrpc": "2.0",
                      "method": "user.login",
                      "params": {
                          "user": UNAME,
                          "password": PWORD},
                      "id": 1
                  })

print(json.dumps(r.json(), indent=4, sort_keys=True))

AUTHTOKEN = r.json()["result"]

template_file_path='/opt/zabbix/template_exported_to_production/'

for file in glob.iglob(template_file_path+'*.xml'): 
      with open(file, 'r') as f:
         data = f.read().replace('\n', '')
         r = requests.post(ZABBIX_API_URL,
                      json={
                          "jsonrpc": "2.0",
                          "method": "configuration.import",
                          "params": {
                              "format": "xml",
                              "rules": {
                                  "templates": {
                                        'createMissing':True,
                                        'updateExisting':True
                                  },
                                  "items": {
                                        'createMissing':True,
                                        'updateExisting':True
                                  },
                                  'triggers': {
                                        'createMissing': True,
                                        'updateExisting': True,
                                  },
                                },
                              "source": data
                            },
                           "auth": AUTHTOKEN

#Logout user
print("\nLogout user")
r = requests.post(ZABBIX_API_URL,
                  json={
                      "jsonrpc": "2.0",
                      "method": "user.logout",
                      "params": {},
                      "id": 2,
                      "auth": AUTHTOKEN
                  })

print(json.dumps(r.json(), indent=4, sort_keys=True))



         
