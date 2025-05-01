radioChannel = 1        # all microbits should be on the same radio channel

# Imports go at the top
from microbit import *
import machine
import struct
import radio
import time
import random

microbitNumber = 0      # each microbit is assigned a number as an easy id for the system
sleepTime = 0           # how long until next disturbance
disturbanceCounter = 0  # number of disturbances

###################################################
## Setup for the radio:
###################################################
radio.config(group=radioChannel)
radio.on()

###################################################
## Setup for the timer
###################################################
currentTime = 0                    # time at a given time
maxWaitMinutes = 0      # max number of minutes between reactions

###################################################
## Setup for actual ID
###################################################
def microbit_friendly_name():
    length = 5
    letters = 5
    codebook = [['z', 'v', 'g', 'p', 't'],['u', 'o', 'i', 'e', 'a'],['z', 'v', 'g', 'p', 't'],['u', 'o', 'i', 'e', 'a'],['z', 'v', 'g', 'p', 't']]
    name = []

    # Derive our name from the nrf51822's unique ID
    _, n = struct.unpack("II", machine.unique_id())
    ld = 1;
    d = letters;

    for i in range(0, length):
        h = (n % d) // ld;
        n -= h;
        d *= letters;
        ld *= letters;
        name.insert(0, codebook[i][h]);

    return "".join(name);
id = str(microbit_friendly_name())

###################################################
## Assisting functions
###################################################

# Function to produce the correct message format with id
def sendMessage(message):
    radio.send(id + "_" + str(message))

# Function to set a new sleep time before next disturbance
def getNewSleepTime():
    maxTime = maxWaitMinutes*60*1000
    minTime = 0
    newSleeptime = random.randrange(minTime,maxTime)+time.ticks_ms()    # new time to react to after current time
    return(newSleeptime)   

# get any relevant information from master microbit
for i in range(3):
    sendMessage("hello")

###################################################
## Loop
###################################################
while True:
    if maxWaitMinutes>0:
        # set new current time
        currentTime = time.ticks_ms()
        # check if sleep time is up
        if currentTime>sleepTime:
            disturbanceCounter = disturbanceCounter+1   # increment disturbance counter
            display.scroll(disturbanceCounter)          # display disturbance counter
            sleepTime = getNewSleepTime()               # set new sleep time
            sendMessage(disturbanceCounter)             # inform master of update
    else:
        sendMessage("hello")
        
    # Listen for radio input
    message = radio.receive()
    if message:
        # Check content of message
        if "wait" in message:
                maxWaitMinutes = int(message.split("_")[1])
        if id in message:
            # "wrong" means the microbit has been reset since start of activity. This message ensures recovery
            if "wrong" in message:
                disturbanceCounter = int(message.split("_")[2])
            # "number" is the assigned id by the system
            if "number" in message:
                microbitNumber = int(message.split("_")[2])

    # to see the assigned id by system, press either button in front to make number scroll
    if button_a.is_pressed() or button_b.is_pressed():
        display.scroll(microbitNumber)
    