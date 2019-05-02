# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 17:34:26 2019

@author: chunt
"""
import matplotlib.pyplot as plt
input = open("wirelessdata.txt")

def convertTime(time):
    time_split = time.split(':')
    hour = time_split[0]
    if time_split[1][2:4] == "AM":
        if hour == "12":
            hour = "00"
        elif int(hour) < 10:
            hour = "0" + hour
    else:
        if int(hour) != 12:
            hour = str(int(hour) + 12)
    return hour + time_split[1][0:2]

def fixTime(time):
    if len(time) == 4:
        if int(time[2:4]) == 60:
            if int(time[0:2]) == 23:
                return "0000"
            if time[0:2] == "09":
                return "1000"
            if time[0:2] == "19":
                return "2000"
            else:
                return time[0] + str(int(time[1]) + 1) + "00"
        if int(time[2:4]) == 75:
            if int(time[0:2]) == 23:
                return "0015"
            if time[0:2] == "09":
                return "1015"
            if time[0:2] == "19":
                return "2015"
            else:
                return time[0] + str(int(time[1]) + 1) + "15"
        else:
            return time
    elif time[2] == "0":
        return time + "0"

#every window is mapped to two different 15 minute time slots
def findTimeSlots(time):
    distancefromslot = int(time[2:4]) % 15
    if distancefromslot < 7:
        firsttime = fixTime(time[0:2] + str(int(time[2:4]) - distancefromslot))
        secondtime = fixTime(time[0:2] + str(int(time[2:4]) - distancefromslot + 15))
    else:
        firsttime = fixTime(time[0:2] + str(int(time[2:4]) - distancefromslot + 15))
        secondtime = fixTime(time[0:2] + str(int(time[2:4]) - distancefromslot + 30))
    return [firsttime, secondtime]
    

timeSlotData = {} #computes aggregate data for each time slot
timeSlotCounts = {} #keeps track of number of times that time slot used, to later  compute that average
#Separate days into intervals of 15 minutes
j = -1
for i in range(96):
    if i % 4 == 0:
        j += 1
        
    minutes = str((i%4)*15)
    if len(minutes) == 1:
        minutes = "0" + minutes
    
    if len(str(j)) == 1:
        timeSlotData["0" + str(j) + minutes] = {"maxclients":0, "maxusagein":0, "maxusageout":0, "avgclients":0, "avgusagein":0, "aveusageout":0}
        timeSlotCounts["0" + str(j) + minutes] = {"maxclients":0, "maxusagein":0, "maxusageout":0, "avgclients":0, "avgusagein":0, "aveusageout":0}
    else:
        timeSlotData[str(j) + minutes] = {"maxclients":0, "maxusagein":0, "maxusageout":0, "avgclients":0, "avgusagein":0, "aveusageout":0}
        timeSlotCounts[str(j) + minutes] = {"maxclients":0, "maxusagein":0, "maxusageout":0, "avgclients":0, "avgusagein":0, "aveusageout":0}

dataOrder = ["maxclients", "maxusagein", "maxusageout", "avgclients", "avgusagein", "aveusageout"]

def splitData(data):
    splitdata = ["",""]
    for i in range(len(data)):
        if data[i].isdigit() or data[i] == ".":
            splitdata[0] = splitdata[0] + data[i]
        else:
            splitdata [1]= splitdata[1] + data[i]
    return splitdata

def convertUnits(data):
    splitdata = splitData(data)
    if splitdata[1] == "Gbps":
        return float(splitdata[0])
    else:
        return (float(splitdata[0]) * .001)

for line in range(288):
    data = input.readline().strip().split(',')
    convertedTime = convertTime(data[0])
    timeSlots = findTimeSlots(convertedTime)
    for i in range(0,6):
        if "Gbps" in data[i + 2] or "Mbps" in data[i+2]:
            timeSlotData[timeSlots[0]][dataOrder[i]] = timeSlotData[timeSlots[0]][dataOrder[i]] + convertUnits(data[i + 2])
            timeSlotCounts[timeSlots[0]][dataOrder[i]] = timeSlotCounts[timeSlots[0]][dataOrder[i]] + 1
            timeSlotData[timeSlots[1]][dataOrder[i]] = timeSlotData[timeSlots[1]][dataOrder[i]] + convertUnits(data[i + 2])
            timeSlotCounts[timeSlots[1]][dataOrder[i]] = timeSlotCounts[timeSlots[1]][dataOrder[i]] + 1
        else:
            timeSlotData[timeSlots[0]][dataOrder[i]] = timeSlotData[timeSlots[0]][dataOrder[i]] + int(data[i + 2])
            timeSlotCounts[timeSlots[0]][dataOrder[i]] = timeSlotCounts[timeSlots[0]][dataOrder[i]] + 1
            timeSlotData[timeSlots[1]][dataOrder[i]] = timeSlotData[timeSlots[1]][dataOrder[i]] + int(data[i + 2])
            timeSlotCounts[timeSlots[1]][dataOrder[i]] = timeSlotCounts[timeSlots[1]][dataOrder[i]] + 1
        

xvalues = range(96)

maxclientslist = []
maxusageinlist = []
maxusageoutlist = []
avgclientslist = []
avgusageinlist = []
aveusageoutlist = []

for val in timeSlotData.keys():
    maxclientslist.append(float(timeSlotData[val]["maxclients"]) / float(timeSlotCounts[val]["maxclients"]))
    maxusageinlist.append(float(timeSlotData[val]["maxusagein"]) / float(timeSlotCounts[val]["maxusagein"]))
    maxusageoutlist.append(float(timeSlotData[val]["maxusageout"]) / float(timeSlotCounts[val]["maxusageout"]))
    avgclientslist.append(float(timeSlotData[val]["avgclients"]) / float(timeSlotCounts[val]["avgclients"]))
    avgusageinlist.append(float(timeSlotData[val]["avgusagein"]) / float(timeSlotCounts[val]["avgusagein"]))
    aveusageoutlist.append(float(timeSlotData[val]["aveusageout"]) / float(timeSlotCounts[val]["aveusageout"]))  

plt.figure(1)
plt.plot(xvalues, maxclientslist)   
plt.plot(xvalues, avgclientslist)
plt.legend(['max clients', 'avg clients'], bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)
plt.xticks([])
plt.show()
#plt.savefig('clientsgraph.png')

plt.figure(2)
plt.plot(xvalues, maxusageinlist) 
plt.plot(xvalues, avgusageinlist)    
plt.plot(xvalues, maxusageoutlist) 
plt.plot(xvalues, aveusageoutlist)
plt.legend(['max bits per second in', 'avg bits per second in', 'max bits per second out', 'avg bits per second out'],bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)
plt.xticks([])
plt.show()  
#plt.savefig('usagegraph.png')
    
    