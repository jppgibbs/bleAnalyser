# Joseph Gibbs | 16014690 | Investigating BLE Privacy Features and Challenges
# 
# Usage:
# 1. Ensure dependencies are installed
# 2. Run with python 2.7 
# 3. Enter scan duration (recommended 30)
# 4. Click start scan
# 5. Once scan is complete, a log file containing the scan data will be saved.
#    Enter the file name into the 'enter log file to graph' field and click genreate graph.

from bluepy.btle import Scanner
import seaborn as sns
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from datetime import datetime
import time
import Tkinter
from collections import defaultdict
from Tkinter import Label, Button, Entry
import json
import unicodedata
import yaml
import numpy as np
import pandas as pd

stop = 1
scans = []
addresses = []
dataVar = []
scanner = Scanner()

# Save Log Function
def saveData():
    # Get current date/time for log title
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y %H_%M_%S.log")
    
    # Save log to disk in json format
    f = open(dt_string, "a")
    f.write(json.dumps(dataVar))
    f.close()

# Scan loop
def scan(iterations):
    # Repeat for the number of times entered in the text box
    for i in range(iterations):
        print('Scanning, iteration = ' + str(i+1))
        devices = scanner.scan(1.0)
        scans.append(devices)
        deviceList = []
        for device in devices:
            deviceList.append({"Address": device.addr, "AddressType": device.addrType, "RSSI": device.rssi})
            # When a new device is discovered, add a new entry
            if device.addr not in addresses:
                addresses.append(device.addr)
            else:
                print "Device Rediscovered"
            print "Device %s (%s), RSSI=%d dB" % (device.addr, device.addrType, device.rssi)
            for (adtype, desc, value) in device.getScanData():
                print "  %s = %s" % (desc, value)
        dataVar.append(deviceList)
    # Save data once scan is complete
    saveData()
    return True

# Stop scan button function
def stopScan():
    stop = 1
    saveData()
    print('stop = ' + str(stop))
# Start scan button function
def startScan():
    stop = 0
    scan(int(e.get()))

def graph(fileName):
    file = open(fileName, mode='r')
    loadedData = file.read()
    file.close()

    addresses = []
    loadedData = yaml.safe_load(loadedData)
    plotData = []
    polls = 1

    for scan in loadedData:
        polls = polls+1
        for device in scan:
            print(device)
            if device['Address'] not in addresses:
                addresses.append(device['Address'])

    print(addresses)

    for address in addresses:
        plotData.append([])
        
    i=0
    for scan in loadedData:
        i=i+1
        for device in scan:
            index = addresses.index(device['Address'])
            plotData[index].append(device['RSSI'])
        for j in range(len(addresses)):
            if len(plotData[j]) < i:
                plotData[j].append(-90)
            

    print(plotData)

    dataFramePrep = { 'x': range(1,polls)}

    for i in range(len(addresses)):
        dataFramePrep[addresses[i]] = plotData[i]

    print(dataFramePrep)

    df=pd.DataFrame(dataFramePrep)

    for i in range(len(addresses)):
        plt.subplot(len(addresses), 1, i+1)
        plt.plot('x', addresses[i], data=df, marker='x', markersize=0, linewidth='2')
        plt.legend(loc='upper left')
    plt.show()


# -- Build UI --
# Create window
window=Tkinter.Tk()
window.minsize(200,250)
window.title("BLE Scanner")

# Create time label
timeLabel = Label(text='Enter scan duration:')
timeLabel.pack()

# Create time entry box
e = Entry(window)
e.pack()
e.focus_set()

# Create start button
startButton = Button(window, text='Start Scanning', command=lambda : startScan())
startButton.config(height = 2, width = 20)
startButton.pack()

# Create stop button
stopButton = Button(window, text='Stop Scanning', command=lambda : stopScan())
stopButton.config(height = 2, width = 20)
stopButton.pack()

# Create time label
graphLabel = Label(text='Enter log file to graph:')
graphLabel.pack()

# Create log file entry box
eGraph = Entry(window)
eGraph.pack()

# Create start button
graphButton = Button(window, text='Generate Graph', command=lambda : graph(str(eGraph.get())))
graphButton.config(height = 2, width = 20)
graphButton.pack()

# Run window
window.mainloop()
