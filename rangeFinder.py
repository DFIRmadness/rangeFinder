#!/usr/bin/python3
'''
AUTHOR: ED-209-Mk7
DATE: 07/29/2109
PURPOSE:  A simple tool to convert results from Trace Route to physical distance.
        Also to experiment with some Python functions.
STATUS:  Much Coffee and motivation.
USAGE: rangeFiner.py [ip or domain]
NOTE:  Range is estimated: 1ms RT is approx. 100 Km (MAX) // Large hops are prob. Space Birds
'''
from sys import exit,argv
from os import  system,geteuid
from subprocess import check_output
from re import compile, findall
from ipaddress import ip_address

if geteuid() != 0:
    print('[!] You must be sudo to use this... ICMP is used for Linux TraceRoute and Requires Sudo..\nExiting...')

TARGET = argv[1]

print('\nRangeFinder v1.0...\n') #ASCII Art in future.

def checkTargetValid(testTarget):
    # Check if Target is IP or Probable Domain name
    try:
        ip_address(testTarget)
        return('Valid IP')
    except ValueError:
        looksLikeDomainRegex = compile('^[a-z0-9\.-]{3,64}\.[a-z]{2,24}$')
        if looksLikeDomainRegex.match(testTarget):
            return('Valid Domain')
        else:
            return('Not Domain or IP')

def argsCheck():# A check if the user is giving a CLI arg
    if len(argv) != 2:
        print('\tUSAGE: '+argv[0]+' [IP OR DOMAIN NAME]\n\tExiting...')
        exit(1)
    print('[i] Checking Target validity...')
    if checkTargetValid(TARGET) == 'Valid IP':
        print('[+] Target detected as IP: '+TARGET+'\n')
    elif checkTargetValid(TARGET) == 'Valid Domain':
        print('[+] Target detected as Domain: '+TARGET+'\n')
    elif checkTargetValid(TARGET) == 'Not Domain or IP':
        print('[-] Target doesn\'t seem to be a domain or IPv4 Address...\nExiting...')
        exit(1)
    else:
        print('[-] An unknown error has occurred with checking the target...\nExiting....')
        exit(1)

totalMaxDistanceToTargetInKMs = float(0)
totalMaxDistanceToTargetInMeters = float(0)

def ranging(targetedSite):
    print('[+] Firing up traceroute...')
    # If windows set commandForTraceR to windows version
    # else go forth with linux
    print('[i] Sending out the probes... pew pew...\n')
    try:        
        traceRouteOut = check_output(['traceroute','-I',targetedSite],text=True).split('\n')
    except:
        print('\nTrace Route Attempt Failed. What did you do!?. The target is probably invalid...\n')
        exit(1)
    if 'traceroute' not in traceRouteOut[0]:
        print('Lazy detection of successful traceroute has indicated a failure...Exiting')
        exit(1)
    else:
        for line in traceRouteOut:
            if 'traceroute' in line or '*' in line:
                print(line)
            else:
                anRTT = compile('([0-9]{1,9}.[0-9]{1,3})\sms') # Select each instance of RTT
                locatedRTTs = anRTT.findall(line)
                if len(locatedRTTs) == 3:
                    rtt1,rtt2,rtt3 = locatedRTTs
                    averagedRTT = (float(rtt1)+float(rtt2)+float(rtt3))/3 #Averaged out the 3 RTT
                    if averagedRTT <= 1:
                        # Less than 1 ms is too low to subtract equipment lag
                        distanceM = averagedRTT * 1000 # Convert ms to Meters
                        global totalMaxDistanceToTargetInMeters
                        totalMaxDistanceToTargetInMeters =+ float(distanceM)
                        distanceM = round(distanceM,1)
                        distanceM = format(distanceM,',')
                        print(line + ' | '+'\x1b[1;32m'+'Max Distance: '+ str(distanceM) + 'Meters'+'\x1b[0m')
                    else:
                        averagedRTT -= 1 # Assuming 1 ms equipment
                        distanceKM = averagedRTT * 100
                        global totalMaxDistanceToTargetInKMs
                        totalMaxDistanceToTargetInKMs =+ float(distanceKM)
                        distanceKM = round(distanceKM,2)
                        distanceKM = format(distanceKM,',')
                        print(line + '| '+'\x1b[1;32m'+'Max Distance: '+str(distanceKM)+' Kilometers'+'\x1b[0m')
                else:
                    print(line)
        totalFinalDistanceinKM = 0
        totalFinalDistanceinKM = float(totalMaxDistanceToTargetInMeters / 1000) + float(totalMaxDistanceToTargetInKMs)
        totalFinalDistanceinKM = round(totalFinalDistanceinKM,3)
        totalFinalDistanceinKM = format(totalFinalDistanceinKM,',') 
        print('\x1b[1;32m'+'Total Maximum Distance to Target is : ' + str(totalFinalDistanceinKM) + '\x1b[0m')
        exit(0)

def main():
    geteuid()
    argsCheck()
    ranging(TARGET)

if __name__ == "__main__":
    main()
else:
    print('Imported...')
    main()
