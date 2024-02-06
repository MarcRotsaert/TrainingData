// var toml = require("toml")
// var concat = require('concat-stream');
// var fs = require("fs")



function showAdapt(cell) {
    var fname = cell.getAttribute("value")
    var url = cell.getAttribute("data-url")
    var elem1 = document.getElementById("rb_delete")
    var elem2 = document.getElementById("rb_update")
    if (elem1.checked) {
        make_xhr("DELETE", fname, url)
        elem1.checked = true
        cell.parentNode.remove()
    }

    else if (elem2.checked) {
        make_xhr("POST", fname, url)
        elem2.checked = true
        toHeadofpage()
    }

}


function showLapdata(cell) {
    var fname = cell.parentNode.getAttribute("value")
    var url = cell.parentNode.getAttribute("data-url")
    console.log(url)
    console.log(fname)

    // Use AJAX to send the data to the Django view
    make_xhr("GET", fname, url)
    toHeadofpage()
}

function make_xhr(hmethod, fname, url) {
    var xhr = new XMLHttpRequest(value = fname);
    if (hmethod === "GET") {
        xhr.open("GET", url, true);
        xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    }

    else if (hmethod === "POST") {
        var csrftoken = getCookie('csrftoken');
        xhr.open("POST", url, true);
        xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }

    else if (hmethod === "DELETE") {
        var csrftoken = getCookie('csrftoken');
        xhr.open("DELETE", url, true);
        xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }

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


function toHeadofpage() {
    window.scrollTo(0, 0);
}

