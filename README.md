# Disturbance Counter
A small project to explore an application of distributing micro:bits to collect and compare changes in micro:bit states.
The concept is based on a workshop on disturbances where micro:bits were used to create random disturbances.
As this project utilises the Buzzer module on the micro:bit, this project is only usable by micro:bit version 2 or later.

# Disturbing a workshop
I will here describe the setup of the project, first by outlining the original activity and then describe how distribution has been applied.

In the original activity, each participant will carry a micro:bit in their pocket for the duration of the activity. Within a set interval, the micro:bit will randomise a delay time to wait before making a disturbance. The number of disturbances each micro:bit has made is stored locally. At the end of the activity the participants are asked to identify the number of disturbances caused by their micro:bit, initiating a discussion session on impact of these disturbances.

In this project this setup has been adapted with a distributed element through the use of the built in radio module on any micro:bit. The facilitator of the activity will have access to a master micro:bit (M-mb) that can inform all the participant-microbits (P-mb) of the max number of minutes to wait before making a disturbance as well as listen for any changes in P-mb states. M-mb is connected to a computer that can through an HTML file display the state of all P-mb, updating the interface as changes are made. If a P-mb is reset, their state can be recovered by the M-mb. 

There is technically no limit to how many P-mb's that can be attached to a single M-mb, however I recommend limiting the activity to max 50 participants. If too many micro:bits are connected, the messages can start built up and block each other, making it difficult to get updates at the right frequency.

# Setting up the activity
Assign one micro:bit as the master micro:bit and upload a HEX version of masterMB.PY onto it. 
All other micro:bits should be assigned participant micro:bits. Upload a HEX version of dummy.py onto it. (The name dummy refers to their ability to be reset and thus not needing to store anything of importance other than their own name)

All python code can be converted to HEX using https://python.microbit.org/. You can either transfer the code to the micro:bit directly through this platform or store the code as a HEX file and drag it onto the micro:bit in your folders. 

Download the index.html and script.js into a folder on your computer. Open the index.html file into a chrome browser (the best one for connecting with micro:bits). As a standard, the maximum number of minutes of delay between disturbances is 1 minute. To change this open the script.js file and change the maxWaitTime parameter to your desired wait time. Save this change and reload the index.html file in your browser. In a later version I will make it possible to change the number of minutes in the index.html file so you do not need to engage with the script.js file at all.

Connect the master micro:bit to the computer and let it stay there for the entire duration of the activity. In the browser, press the "start" button. Connect battery packs to any number of P-mbs.
