# bleAnalyser
Python Bluetooth Low Energy scanning and visualisation tool

Software tested on Kali Liux 2019.4 
Ensure you are using python 2.7.16

Install dependencies:

apt-get install python-tk
apt-get install python-pip libglib2.0-dev

pip install bluepy
pip install seaborn
pip install pyyaml
pip install matplotlib
pip install numpy
pip install pandas


Ensure device has bluetooth enabled and supports BLE (4.0)


# Usage Guide

Usage:
 1. Ensure dependencies are installed
 2. Run with python 2.7 - 'python bleAnalyser.py'
 3. Enter scan duration (recommended 30)
 4. Click start scan
 5. Once scan is complete, a log file containing the scan data will be saved.
    Enter the file name into the 'enter log file to graph' field and click generate graph.

Note: I have included a sample log file '21_02_2020 17_24_42.log' with some pre-recorded data.
