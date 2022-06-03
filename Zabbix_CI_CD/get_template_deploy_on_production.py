from pyzabbix.api import ZabbixAPI, ZabbixAPIException
from sys import exit
from datetime import datetime
import argparse,os,json,xml.dom.minidom

zabbix_url="http://zabbix.local/zabbix"
zabbix_user="Zabbix_API"
zabbix_password="password"

zapi = ZabbixAPI(url=zabbix_url,user=zabbix_user,password=zabbix_password)
print("Connected to Zabbix API Version %s" % zapi.api_version())

templateIDs=[]
templateID = zapi.template.get(output='extend', tags=[{"tag":"ENV","value":"PROD"}])

if len(templateID) > 0:
   for tpl in templateID:
      print(tpl['templateid'])
      zbxxml = zapi.configuration.export(options={'templates':[format(tpl['templateid'])]},format='xml')
      dest = '/opt/zabbix/template_exported_to_production/'+tpl['host']+'.xml'
      template = xml.dom.minidom.parseString(zbxxml.encode('utf-8'))
      date = template.getElementsByTagName("date")[0]
      date.firstChild.replaceWholeText('2016-01-01T01:01:01Z')
      f = open(dest,'wb')
      f.write(template.toprettyxml().encode('utf-8'))
      f.close()
