#!/usr/bin/python3
'''
AUTHOR: ED-209-Mk7
DATE: 06/28/2108
PURPOSE:  A simple tool to convert results from Trace Route to physical distance.
        Also to experiment with some Python functions.
STATUS:  Much Coffee and motivation.
USAGE: rangeFiner.py [ip or domain]
NOTE:  Range is estimated: 1ms RT is approx. 100 Km (MAX) // Large hops are prob. Space Birds
'''
import sys #clean exits
import os #file manipulation
#import subprocess #Executing commands
import re

print('\nRangeFinder v.01...\n') #ASCII Art in future.

def argsCheck():# A check if the user is giving a CLI arg
    global theTgt #Set up global var theTgt
    if len(sys.argv) != 2:
        print('\tUSAGE: '+sys.argv[0]+' [IP OR DOMAIN NAME]\n')
        sys.exit(1)
    else:#If Checks are passed then set a global Var for use later. Print to show.
        theTgt = sys.argv[1]
        print('Target set to: '+theTgt+'\n')

def ranging():
    #Execute traceroute to target provided by arg1 and place into rangeFinder.tmp
    #Setup a file to write to...
    try:
        tmpFile = open('rangeFinder.tmp','w', encoding="utf-8")
        #Send Traceroute to the Target
        print('Executing: Traceroute '+ str(theTgt)+'\n')
        cmd = 'traceroute '+theTgt+' | tee rangeFinder.tmp'
        print('Showing Original Traceroute...\n')
        os.system(cmd) #Actual command execution
        print('\nRanging Complete.'+'\n')
        tmpFile.close()
    except:
        print('Error occurred while attempting ranging to the target...')
        sys.exit(1)


def textInteract():
    try:
        #Copy rangeFinder.tmp to rangeFinder2.tmp
        print('\nCopying Traceroute output to another file for manipulation.'+'\n')
        os.system('cp rangeFinder.tmp rangeFinder2.tmp')
        #Change the RTT from ms to Km in rangeFinder2.tmp (Take that time and multiply by 100 Km.)
        #REGEX to select only RTT is: '([0-9]{1,9}\.[0-9]{1,3})\sms'
        with open('rangeFinder2.tmp') as file:
            line=file.readline() #lines are read from the open file per line
            for line in file: #for each line do some stuff
                #remove new-line or return-line from end of line
                line = line.rstrip()
                rtt=re.compile('([0-9]{1,9}\.[0-9]{1,3})\sms') # Select each instance of RTT
                findRtt = rtt.findall(line)
                if len(findRtt) < 3: # If there is no RTT located skip the line
                    #print(line)
                    continue
                else: # If it found 3 RTT then go ahead and massage them.
                    rtt1,rtt2,rtt3 = findRtt #Times are each instance of RTT
                    #line = line.strip(str(findRtt))
                    averagedRTT = (float(rtt1)+float(rtt2)+float(rtt3))/3 #Averaged out the 3 RTT
                    #If less than 1 ms it will be less than 100 KM
                    if averagedRTT <= 1:
                        # Less than 1 ms is too low to subtract equipment lag
                        distanceM = averagedRTT * 1000 # Convert ms to Meters
                        distanceM = round(distanceM,1)
                        distanceM = format(distanceM,',')
                        print(line + ' | '+'\x1b[1;32m'+'Max Distance: '+' '+str(distanceM)+' Meters'+'\x1b[0m')
                        continue
                    else:
                        averagedRTT -= 1 # Assuming 1 ms equipment
                        distanceKM = averagedRTT * 100
                        distanceKM = round(distanceKM,2)
                        distanceKM = format(distanceKM,',')
                        print(line + '| '+'\x1b[1;32m'+'Max Distance: '+str(distanceKM)+' Kilometers'+'\x1b[0m')
                #Future ideas:
                #Remove 3 RTT's and instead display the average RTT and Distance
                #Increment Global RTT Val
    except:
        print('An error occurred attempting to produce the report...')
        sys.exit(1)

def cleanUp():
    try:
        print('\nCleaning tmp files up.')
        os.system('rm rangeFinder.tmp rangeFinder2.tmp')
    except:
        print('An error occurred while attempting to clean up the tmp files...')
        sys.exit(1)


def main():
    argsCheck()
    ranging()
    textInteract()
    cleanUp()
    sys.exit(0)

if __name__ == "__main__":
    main()
else:
    print('Imported...')
    main()
