// values to establich serial connection with the microbit
let port;
let writer;
let reader;

let messageConstruct = [];  // array to construct messages from the microbit
let maxWaitTime = 1;

// locally store any information received from the microbit
let knownMicrobits = [[],[],[]]; // [0] are the actual microbit names, [1] are the assigned numerical id's, [2] are the values stored

// a bar chart on the computer interface
const ctx = document.getElementById('myChart');

let mychart = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: knownMicrobits[1],  // The labels in the chart are the assigned id's which can be found on the microbit by pressing a or b
    datasets: [{
      label: 'Forstyrrelser',
      data: knownMicrobits[2],  // The data is the values for each microbit
      borderWidth: 1
    }]
  },
  options: {
    scales: {
      y: {
        beginAtZero: true
      }
    }
  }
});

/**
 * Function to live update the chart with any new information
 * @param {int} label   The assigned id of the microbit
 * @param {str} id      The actual id of the microbit
 * @param {int} value   The number of disturbances
 */
function updateChart(label, id, value) {
  // First check if this microbit is already known
  let newMicrobit = true;
  let microbitIndex = 0;
  for(let i=0; i<knownMicrobits[0].length;i++){
    if(knownMicrobits[0][i]==id){
      newMicrobit = false;
      microbitIndex = i;
    }
  }
  // If this is a new microbit, locally store the values, else just update the value parameter
  if(newMicrobit){
    knownMicrobits[0].push(id);
    knownMicrobits[1].push(label);
    knownMicrobits[2].push(value);
    console.log(knownMicrobits);
  } else {
    knownMicrobits[2][microbitIndex] = value;
  }
  // Update the chart
  mychart.update();
}

/** 
 * Listening for any interaction with the button on the computer interface
 * If a connection has not yet been established, this button will intiate a connection
 * If a connection has been established, this button will simply ask for any information from the microbit
*/
document.getElementById("startbutton").addEventListener("click",event=>{
  let sleeptime = maxWaitTime.toString()
  writeToMB("sleep_" + sleeptime);
});


/**
 * Send a string to the micro:bit
 * If the connection has not been established by the start of the program, we establish it here.
 * @param {str} message   The message to transfer to the microbit
 */
async function writeToMB(message){
  //event.preventDefault();
  if (!port) {
    port = await navigator.serial.requestPort();
    await port.open({ baudRate: 9600 });
    writer = port.writable.getWriter();
    reader = port.readable.getReader();
    console.log(typeof(navigator.serial.requestPort()))
    readLoop();
  }
  // All messages sent starts with "__" and ends with "_" to allow the micro:bit to decode the message along with relevant meta data
  const data = new TextEncoder().encode("__" + message + "_" + '\n');
  await writer.write(data);
}

/**
 * Read the serial input from the microbit. The function only reads one character at a time, which are stored in the global messageConstruct array.
 * All messages are constructed by starting with a "#"" and ending with a "&" - looking for these characters allows us to identify when a complete message has been sent.
*/
async function readLoop() {
  while (true) {
    const { value, done } = await reader.read();
    if (value) {
        let collectedInput = new TextDecoder().decode(value);
        if(collectedInput == "#"){
            // Clean list of collected characters
            while (messageConstruct.length > 0) {
                messageConstruct.pop();
            }
        }
        else if(collectedInput == "&"){
            // Construct a message from the list of collected characters
            let output = messageConstruct.toString().split(",").join("")
            // Now we check what is in the message we have constructed
            checkMessage(output)
        }
        else{
            // Add to list of collected characters
            messageConstruct.push(collectedInput)
        }
    }
    if (done) {
      reader.releaseLock();
      break;
    }
  }
}

/**
 * Function to check the received message
 */
function checkMessage(message){
  if(message.substr[0,5] == "sleep"){
    writeToMB("sleep_" + maxWaitTime.toString())
  }
  microbitName = message.split("_")[0];
  microbitId = message.split("_")[1];
  microbitValue = message.split("_")[3];
  if(microbitName.substr[0,1]=="#"){
    console.log("whoops");
    return;
  }
  updateChart(microbitName, microbitId, parseInt(microbitValue));
}