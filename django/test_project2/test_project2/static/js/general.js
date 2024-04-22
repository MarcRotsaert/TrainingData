function toHeadofpage() {
    window.scrollTo(0, 0);
}

// Function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
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


function make_xhr(hmethod, fname, url, data) {
    let xhr = new XMLHttpRequest(value = fname);
    if (hmethod === "GET") {
        xhr.open("GET", url, true);
        xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    }
    else {
        console.log(hmethod)
        const csrftoken = getCookie('csrftoken');
        xhr.open(hmethod, url, true);
        xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            // Handle the response from the server if needed
            console.log(xhr.responseText);
            const newHTML = xhr.responseText;
            document.open();
            document.write(newHTML);
            document.close();

        }
    };

    let requestData = { "fname": fname }
    if (data) {
        Object.assign(requestData, data)
    }
    let jsonData = JSON.stringify(requestData);
    xhr.send(jsonData);
}
