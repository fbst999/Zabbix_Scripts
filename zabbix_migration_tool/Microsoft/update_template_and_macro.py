#####################################################
### to launch with command python 3 script.py
###
### The purpose of this script is to import data
### from a csv file with the following achitecture
### hostname | hostname/Instance | Port
### These data will be processed to be used to
### generate user macros into the hostname put in
### the file
### It will also get all the current template
### save them into a list and add a specific template
### The id of the template needs to be filled in the
### template_id_to_add variable
#####################################################

from pyzabbix.api import ZabbixAPI, ZabbixAPIException
import sys, csv

###############################
### Variables
###############################
ZabbixServerUrl="https://zabbix-server.local"
ZabbixUser="Zabbix"
ZabbixPassword="Password"


zapi = ZabbixAPI(url=ZabbixServerUrl,user=ZabbixUser,password=ZabbixPassword)
print("Connected to Zabbix API Version %s" %zapi.api_version())

####################################################
### Imported data from CSV File:
###    - Host
###    - shortname/Instance
###    - Port
####################################################


mssql_data_input_path = "Path_to_csv_file"
template_id_to_add = {'templateid':ID}

currentTemplates={}

####################################################
### Read CSV File and return host, instance name 
### and port
####################################################

def readFile():
   csvfile = open(mssql_data_input_path,'r')
   csvfile = csv.reader(csvfile,delimiter='|')
   for [host,instance,port] in csvfile:
       instanceName=instance.split('\\')
       instanceName=instanceName[1]
       yield host,instanceName,port

####################################################
### Gather the current templates
### attached to the hosts
### return dict with templates and list of hostids
####################################################

def getCurrentTemplates():
    hosts=[]
    hostids=[]
    for dbinfo in readFile():
        TeamplatesInfos={}
        hosts.append(dbinfo[0])
        zhost = zapi.host.get(filter=({"host":dbinfo[0]}),output=['name','hostid'],selectParentTemplates=['templateid'])
        hostids.append(zhost[0]['hostid']
        TemplatesInfos=zhost[0]['parentTemplates']
        currentTemplates[zhost[0]['hostid']]=TemplatesInfos
    yield currentTemplates,hostids


###################################################
### get the current templates and add in the dict
### the informations related to the new template
### to add
###################################################

def addMSSQLTemplate():
   for i in getCurrentTemplates():
      for j in range(0,len(i[1])):
         templateList=[]
         Template_to_add=[]
         templateList=i[0][i[1][j]]
         templateList.append(template_id_to_add)
         for k in range(0,len(templateList)):
            Template_to_add.append(templateList[k]['templateid'])
            zhost = zapi.host.update(hostid=i[1][j],templates=Template_to_add)

###################################################
### 1) define a dict with the values gathered in 
### the CSV file
### 2) check if the macro already exist
###    if exist: update the value
###    if not: create the macro
###################################################

def createMacros():
   macros={}
   for i in readFile():
      for j in getCurrentTemplates():
         for k in range(0,len(j[1])):
            macros['{$MSSQL.AGENT.SERVICE}']='SQLAgent$'+i[1]
            macros['{$MSSQL.INSTANCE}']='MSSQL$'+i[1]
            macros['{$MSSQL.PORT}']=i[2]
         for keys,values in macros.items():
            zhost = zapi.host.get(filter=({"host":i[0]},output='hostid')
            hostid = zhost[0]['hostid']
            zhost2 = zapi.usermacro.get(filter=({"hostid":hostid,"macro":keys}),output='extend')
            if len(zhost2)>0:
               macroid=zhost2[0]['hostmacroid']
               zhost4 = zapi.usermacro.update(hostmacroid=macroid,value=values)
            else:
               zhost3 = zapi.usermacro.create(hostid=hostid,maco=keys,value=values)

####################################################
### Functions Call
####################################################

createMacros()
addMSSQLTemplate()
