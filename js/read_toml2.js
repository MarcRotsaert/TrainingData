// var toml = require("toml")
// var concat = require('concat-stream');
// var fs = require("fs")



// script.js

// Define a function that updates the content of the "demo" paragraph
function updateDemo() {
    var demoElement = document.getElementById("button");
    demoElement.innerHTML = "Hello, World! (from a function)";
}

function selectText2() {
    var testElement = document.getElementById("trainingtype")
    console.log(testElement.value)
}


// Add an event listener to call the function when the button is clicked
document.getElementById("button").addEventListener("click", selectText2);


function read_toml() {

    // Specify the path to your TOML file
    const tomlFilePath = "config_dummy.toml";

    // Create a read stream for the TOML file
    const readStream = fs.createReadStream(tomlFilePath, 'utf8');

    let data = '';

    readStream.on('data', (chunk) => {
        data += chunk;
    });

    readStream.on('end', () => {
        // Now, the `data` variable contains the entire contents of the TOML file as a string
        console.log(data);

        // You can parse it as TOML if needed
        const toml = require('toml');

        try {
            parsedData = toml.parse(data);
        } catch (e) {
            console.error("Parsing error on line " + e.line + ", column " + e.column +
                ": " + e.message);
        }

        // Now you can work with the parsed TOML data
        console.log(parsedData["garmin_fit"]["paramnameconversion"]);

    });

    readStream.on('error', (err) => {
        console.error(`Error reading TOML file: ${err}`);
    });
    return data
}
