##############################################################################
### script usage: python3 check_agent_availability.py <inputfile> <outputfile>
##############################################################################
import pyzabbix.api import ZabbixAPI
import sys, csv

############################################################
### Variables
############################################################
Zabbix_url='http://zabbix.local'
Zabbix_user='Zabbix_API'
Zabbix_password='password'

inputfile = sys.argv[1]
inputfile = open(inputfile,"r")
inputfile = csv.read(inputfile)

outputfile = sys.argv[2]

###########################################################
### API Authentication
###########################################################
zapi = ZabbixAPI(url=Zabbix_url,user=Zabbix_user,password=Zabbix_password)

###########################################################
### read the csv file and extract hosts
### if host is in fqdn format, the script will extract 
### the short name in cas of zabbix host field gathered
### with host short name
###########################################################
for [host] in inputfile:
    newhost=host.lower()
    shortname = newhost.split(".")
    shortname = shortname[0]
    ### get the host read in the current line of the file with fqdn
    zhost = zapi.host.get(output=['host','name','status','available'],filter={"host":newhost})
    ### get the host read in the current line of the file with shortname
    zhost2 = zapi.host.get(output=['host','name','status','available'],filter={"host":shortname})
    ### if no response with fqdn and that we have something with the shortname
    ### then identified the status of the current host
    if(len(zhost))>0 and (len(zhost2))==0:
        if(zhost[0]['available']=='0'):
            host_status = 'Host is disabled in zabbix'
        elif(zhost[0]['available']=='1'):
            host_status = 'Zabbix agent is ONLINE'
        elif(zhost[0]['available']=='2'):
            host_status = 'Zabbbix agent is OFFLINE'
        print(newhost+" exist in zabbix"+host_status)
        str = newhost + " | exist in zabbix | "+host_status
        ### write the results in a file with | as a separator 
        ### to be able to filter the informations in excel or other
        with open(outputfile,'a') as fd:
            writer_object = csv.writer(fd)
            writer_object.writerow([str])
    ### if no result with shortname and that we have something with the fqdn
    ### then identified the status of the current host
    elif(len(zhost2))>0 and len(zhost)==0:
        if(zhost2[0]['available']=='0'):
            host_status = 'Host is disabled in Zabbix'
        elif(zhost2[0]['available']=='1':
            host_status = 'Zabbix agent is ONLINE'
        elif(zhost2[0]['available']=='2':
            host_status = 'Zabbix agent is OFFLINE'
        print(newhost + " exist in zabbix"+host_status)
        str = newhost + " | exist in zabbix | "+host_status
        ### write the result in a file
        with open(outputfile,'a') as fd:
           writer_object = csv.writer(fd)
           writer_object.writerow([str])
    ### if no result with fqdn and shortname
    ### then the host does not exist in zabbix
    elif(len(zhost)==0) and (len(zhost2)==0):
       print(newhost + " does not exist in zabbix")
       str = newhost + " | not exist in zabbix"
       ### write the status in file
       with open(outputfile,'a') as fd:
          writer_object = csv.writer(fd)
          writer_object.writerow([str])
