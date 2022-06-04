##################################################################
### Script usage: python3 export_templates.py <output_folder> 
### the script will export all templates in Zabbix and write 
### xml file in the output folder given in parameter
##################################################################

import argparse,logging,time,os,json,xml.dom.minidom

from pyzabbix import ZabbixAPI
from sys import exit
from datetime import datetime

Zabbix_url = "http://zabbix.local"
Zabbix_user = "Zabbix_API"
Zabbix_password = "password"

outputPath=sys.argv[1]

zapi = ZabbixAPI(Zabbix_url,user=Zabbix_user,password=Zabbix_password)

zbxtemplate = zapi.template.get(output="extend")
for template in zbxtemplate:
    zbxxml = zapi.configuration.export(options={'templates':[format(h['templateid'])]},format='xml')
    dest = outputPath+template['host']+'.xml'
    print(template['host']+".xml")

    template = xml.dom.minidom.parseString(zbxxml.encode('utf-8')
    date = template.getElementsByTagName("date")[0]
    date.firstChild.replaceWholeText('2016-01-01T01:01:01Z')
    f = open(dest, 'wb')
    f.write(template.toprettyxml().encode('utf-8'))
    f.close()


