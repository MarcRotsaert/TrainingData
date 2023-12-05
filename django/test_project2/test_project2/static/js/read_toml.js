var toml = require("toml")
var concat = require('concat-stream');
var fs = require("fs")
stream = fs.createReadStream("config.toml", 'utf8')

stream.on('data', (chunk) => { data += chunck; })

stream.on('end', () => {
    try {
        // Parse the TOML data
        const parsedData = toml.parse(data);

        // Now you can work with the parsed TOML data
        console.log(parsedData);
    } catch (parseError) {
        console.error(`Error parsing TOML: ${parseError}`);
    }
});

stream.on('error', (err) => {
    console.error(`Error reading TOML file: ${err}`);
});

// console.log(parsed)
// parsedtext = toml.parse("config.toml")
// console.log(parsedtext)