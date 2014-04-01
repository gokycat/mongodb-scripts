#!/usr/bin/python

##---- SCRIPT TO DISPLAY MONGO CLUSTER STATUS ----##

import pymongo
from ConfigParser import SafeConfigParser
from progressbar import ProgressBar
pbar = ProgressBar()

##connect to mongos host:
def mongos_connect(host, port):
    try:
        client = pymongo.MongoClient(host, port)
        db = client.config
        collection = db.shards
        shards = collection.find()
        return shards
    except Exception, e:
        print "Unable to connect to the mongo host"
        print e

##grep replica sets from shards_info
def getReplicas(shards):
    replicas = {}
    for rs in shards:
        rs_name = rs['_id']
        rs_mems = rs['host'].split('/')[1]
        replicas[rs_name] = rs_mems
    return replicas

##prints replica sets:
def printReplicas(reps):
    for k, v in pbar(sorted(reps.iteritems())):
        print k + " : " + v

##main function:
def main():
    ## config_data.ini file location, as it is in the same directory just the filename is enough. 
    default_config_file = 'config_data.ini'
    parser = SafeConfigParser()
    parser.read(default_config_file)
    mongos_host = str(parser.get('default', 'mongos_host'))
    mongos_port = int(parser.get('default', 'mongos_port'))
    shards_info = mongos_connect(mongos_host, mongos_port)
    #get replica sets info.
    rsets = getReplicas(shards_info)
    printReplicas(rsets)


if __name__ == '__main__':
    main()

