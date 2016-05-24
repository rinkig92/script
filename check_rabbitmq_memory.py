#!/usr/bin/env python2.7
# Author : 
# Version: 1.0.0

import sys, os, json
import requests
from optparse import OptionParser

### Constant ###
EXIT_NAGIOS_OK = 0
EXIT_NAGIOS_WARN = 1
EXIT_NAGIOS_CRITICAL = 2
EXIT_NAGIOS_UNKNOWN = 3
mem_used = 0

def getMemory(host, domain, port, user, password):

    try:
        url = "http://"+host+"."+domain+":"+str(port)+"/api/nodes/rabbit@"+host +"?memory=true"
        getData = requests.get(url,auth=(user,password)).json()
        usedMemory = getData["mem_used"] / 1024 / 1024
        return usedMemory
    except requests.ConnectionError as e:
        print ("ConnectionError. Unable to connect to host  %s" %host)
        sys.exit(EXIT_NAGIOS_UNKNOWN)
    except requests.exceptions.RequestException as e:
        print e
        sys.exit(EXIT_NAGIOS_UNKNOWN)
    except:
        print("An unknown exception occured..")
        sys.exit(EXIT_NAGIOS_UNKNOWN)

def getOption():
    global critical_threshold
    global warn_threshold

    parser = OptionParser(usage="Usage: %prog [options]", version="%prog 1.0")
    parser.add_option("-H", "--host", dest="host", default=None, help="RabbitMQ Host i.e. alpcispmq822v")
    parser.add_option("-d", "--domain", dest="domain", default="corporate.ge.com", help="RabbitMQ Host i.e. corporate.ge.com")
    parser.add_option("-P", "--port", dest="port", type="int", default=15672, help="RabbitMQ Port i.e. 15672")
    parser.add_option("-u", "--user", dest="user", default=None, help="RabbitMQ user")
    parser.add_option("-p", "--pass", dest="password", default=None, help="RabbitMQ password")
    parser.add_option("-w", "--warn", dest="warn_threshold",type="int", default=250, help="Memory utlization (in MB) that triggers a warning status.")
    parser.add_option("-c", "--critical", dest="critical_threshold",type="int", default=300, help="Memory utlization (in MB) that triggers a critical status.")
    (options, args) = parser.parse_args()
    warn_threshold = options.warn_threshold
    critical_threshold = options.critical_threshold
    variables="host domain port user password".split()
    for r in variables:
        if options.__dict__[r] is None:
            parser.error("Parameter Error !!! %s is required" %r)
            sys.exit(-1)
    return getMemory(options.host, options.domain, options.port, options.user, options.password)

if __name__ == '__main__':
    mem_used = getOption()
    if mem_used >= critical_threshold:
        print ("CRITICAL: RabbitMQ is using %d MB of RAM." %mem_used)
        sys.exit(EXIT_NAGIOS_CRITICAL)
    elif mem_used >= warn_threshold:
        print ("WARNNING: RabbitMQ is using %dMB of RAM." %mem_used)
        sys.exit(EXIT_NAGIOS_WARN)
    print ("OK: RabbitMQ is using %dMB of RAM." %mem_used)
    sys.exit(EXIT_NAGIOS_OK)
