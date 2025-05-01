radioChannel = 1

# Imports go at the top
from microbit import *
import radio
uart.init()


knownMicrobits = []         # list of active micro:bits
maxWaitMinutes = 0      # max number of minutes between reactions from small microbits
display.show(Image.HAPPY)

###################################################
## Setup for the radio:
###################################################
radio.on()
radio.config(group=radioChannel, power=7)

###################################################
## Assisting functions
###################################################

# Function to produce the correct message format for the computer
def writeToComputer(message):
    print("#" + str(message) + "&")

###################################################
## Loop
###################################################
while True:
    if maxWaitMinutes < 1:
        writeToComputer("sleep")
    
    # Listen for serial input
    if uart.any():
        # Give time for the full message to be received
        sleep(300)
        uartmessage = str(uart.readline())
        if 'start' in uartmessage:      # Only one button on inderface, so when pressed the microbit will update the computer with any information it has.
            for i in range(len(knownMicrobits)):
                microbitIndex = i+1
                writeToComputer(str(microbitIndex) + "_" + knownMicrobits[microbitIndex][0] + "_number_" + str(knownMicrobits[microbitIndex][1]))
        if "sleep" in uartmessage:
            maxWaitMinutes = int(uartmessage.split("_")[3])
    
    # Listen for radio input
    message = radio.receive()
    if message:
        if "hello" in message:
            if maxWaitMinutes>0:
                radio.send("wait_" + str(maxWaitMinutes))
        else:
            microbitID = str(message.split("_")[0])     # get the id of the microbit
            receivedValue = str(message.split("_")[1])  # get the value of the microbit
            # Check if microbit is already known by system
            microbitIndex = 0
            microbitUnknown = True
            for i in range(len(knownMicrobits)):
                if knownMicrobits[i][0] == microbitID:      # If known, update the value locally
                    if int(receivedValue) > int(knownMicrobits[i][1]):  # If the new value is bigger than the currently stored value, the value is simply updated locally
                        knownMicrobits[i][1] = receivedValue
                    else:   # If the new value is smaller than the currently stored value, the child has accidentally reset their microbit, restarting the counter.
                        knownMicrobits[i][1] = str(int(knownMicrobits[i][1]) + 1)
                        radio.send(microbitID + "_wrong_" + str(knownMicrobits[i][1]))  # We inform the microbit of the error and send an incrementation of currently stored value
                        microbitNumber = i+1
                        radio.send(microbitID + "_number_" + str(microbitNumber))       # We reassign the microbit their numerical id
                    microbitIndex = i
                    microbitUnknown = False
            if microbitUnknown:     # If this is a new microbit
                knownMicrobits.append([microbitID,receivedValue])   # We add the microbit information locally
                microbitIndex = len(knownMicrobits)-1
                for i in range(3):
                    radio.send(microbitID + "_number_" + str(len(knownMicrobits)))  # We assign the microbit a numerical id
            microbitIndex +=1
            writeToComputer(str(microbitIndex) + "_" + microbitID + "_number_" + str(knownMicrobits[microbitIndex][1])) # Finally, we update the computer with any new information