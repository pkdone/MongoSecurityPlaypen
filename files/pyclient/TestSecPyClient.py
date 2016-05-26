#!/usr/bin/env python
import sys
import ssl 
import urllib
from pymongo import MongoClient
 
###
# Main function to query database
###
def main():
    print 
    print "--STARTED: Secure test client python script"
    print 

    try: 
        connectionURL = getConnectionURL()
        print "--MONGODB CONNECTION URL:  %s" % connectionURL
        print 

        # If using cert authenticaiton, problem passing "cert required" param in URL, so passing explicitly here
        if (client_auth_method == 'cert'): 
            client = MongoClient(connectionURL, ssl_cert_reqs=ssl.CERT_REQUIRED)
        else: 
            client = MongoClient(connectionURL)

        db = client.maindata
        collection = db.records

        for record in collection.find({"age": {"$gt": 40}}):
            print " ** Person with age over 40 found - name: %s **   " % record['name']
    except:
        print "  Unexpected error: %s  " % sys.exc_info()[1]

    print 
    print "--FINISHED: Secure test client python script"
    print


###
# Builds MongoDB connection string depending on security settings 
###
def getConnectionURL():
    rep_set_member_count = 3
    connectionURL = 'mongodb://'

    if client_auth_method == 'userpwd' or client_auth_method == 'ldap':
        connectionURL += db_sampleuser_name + ':' + db_sampleuser_password + '@'
    elif client_auth_method == 'cert':
        connectionURL += '%s@' % urllib.quote_plus('CN=' + db_sampleuser_name + client_dn_suffix)
    elif client_auth_method == 'kerberos':
        # @ sign needs to be escaped to %40 to avoid clashing with URL @ sign usage later on in URL
        connectionURL += db_sampleuser_name + '%40' + uppercase_org_name + '.' + uppercase_org_type + '@'

    isFirst = True

    for replica in range(0, rep_set_member_count):
        if not isFirst:
            connectionURL += ','

        connectionURL += 'dbnode' + str(replica + 1) + '.vagrant.dev:27017'
        isFirst = False

    connectionURL += '/?replicaSet=' + rep_set_name

    if sslEnabled or client_auth_method == 'cert':
        connectionURL += '&ssl=true&ssl_ca_certs=/etc/ssl/mongodbca.pem'

    if client_auth_method == 'userpwd':
        connectionURL += '&authMechanism=SCRAM-SHA-1'
    elif client_auth_method == 'ldap':
        connectionURL += '&authMechanism=PLAIN&authSource=$external'
    elif client_auth_method == 'cert':
        # When adding, the following pymongo errors - why?: &ssl_cert_reqs=ssl.CERT_REQUIRED
        connectionURL += '&authMechanism=MONGODB-X509&ssl_certfile=/home/vagrant/sampleuser_client.pem'
    elif client_auth_method == 'kerberos':
        connectionURL += '&authMechanism=GSSAPI'

    return connectionURL


# Quick and dirty array for testing if some text is true
trueStrings = ['true', 'True', 'TRUE', '1']

# Pre-populated global variables
rep_set_name = '{{ rep_set_name }}'
sslEnabled = '{{ ssl_enabled }}' in trueStrings
client_auth_method = '{{ client_auth_method }}'
db_sampleuser_name = '{{ db_sampleuser_name }}'
db_sampleuser_password = '{{ db_sampleuser_password }}'
client_dn_suffix = '{{ client_dn_suffix }}'
uppercase_org_name = '{{ org_name|upper }}'
uppercase_org_type = '{{ org_type|upper }}'


if __name__ == "__main__":
    main()


