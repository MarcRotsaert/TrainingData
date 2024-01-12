// var toml = require("toml")
// var concat = require('concat-stream');
// var fs = require("fs")



// script.js

// Define a function that updates the content of the "demo" paragraph
function updateDemo() {
    var demoElement = document.getElementById("button");
    demoElement.innerHTML = "Hello, World! (from a function)";
}

function updatePlaatje() {
    // image = document.getElementsByClassName("grafiek")[0]
    image = document.getElementById("grafje")

    // console.log('change pictures')
    var val = selectText2()
    switch (val) {
        case "easy":
            image.src = "/static/images/knmirotterdam_220616_11.png"
            console.log(1);
            break;
        case "interval":
            image.src = "/static/images/knmirotterdam_220719_15.png"
            console.log(2);
            break;
        case "road":
            image.src = "/static/images/knmirotterdam_220814_07.png"
            console.log(3);

    }
}

function updateText2() {
    console.log("grrr")
    var textvalue = selectText2()
    elem = document.getElementById("textblok")
    elem.innerHTML = textvalue
}

function selectText2() {
    var testElement = document.getElementById("trainingtype")
    console.log(testElement.value)
    console.log('BlaBla')
    return testElement.value
}

function showForm(cell) {
    var fname = cell.parentNode.getAttribute("value")
    var url = cell.parentNode.getAttribute("data-url")
    var csrftoken = getCookie('csrftoken');
    console.log(url)
    var xhr = new XMLHttpRequest(value = fname);
    cell.fname = fname
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.setRequestHeader("X-CSRFToken", csrftoken);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            // Handle the response from the server if needed
            console.log(xhr.responseText);
            var newHTML = xhr.responseText;
            document.open();
            document.write(newHTML);
            document.close();

        }
    };

    var jsonData = JSON.stringify({ "fname": fname });
    xhr.send(jsonData);
    toHeadofpage()
    // return fname

}

function showLapdata(cell) {
    // console.log(cell.parentNode.id)
    var fname = cell.parentNode.getAttribute("value")
    var url = cell.parentNode.getAttribute("data-url")
    var csrftoken = getCookie('csrftoken');
    console.log(url)
    // console.log(fname)
    // Use AJAX to send the data to the Django view
    var xhr = new XMLHttpRequest(value = fname);
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.setRequestHeader("X-CSRFToken", csrftoken);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            // Handle the response from the server if needed
            console.log(xhr.responseText);
            var newHTML = xhr.responseText;
            document.open();
            document.write(newHTML);
            document.close();

        }
    };

    var jsonData = JSON.stringify({ "lapdata": fname });
    xhr.send(jsonData);
    toHeadofpage()
    // return fname
}

// Function to get CSRF token from cookies
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Add an event listener to call the function when the button is clicked
// document.getElementById("button").addEventListener("click", selectText2);

function toHeadofpage() {
    window.scrollTo(0, 0);
}

