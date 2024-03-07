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

function plotLapdata(cell) {
    var fname = cell.getAttribute("value");
    var url = cell.getAttribute("data-url");
    console.log(fname)
    console.log(url)

    // fetch(url + "?fname=" + fname)
    // fetch(url + fname)
    fetch(url)
        .then(response => response.json())
        .then(data => {
            // Process the retrieved data and plot using Chart.js
            // console.log(data)
            plotje(data)
                ;
        })
        .catch(error => console.error('Error:', error));
}


function createDataset(valArray, duration) {
    const totalDuration = duration.reduce((total, duration) => total + duration, 0);
    const barPercentages = duration.map(duration => duration / totalDuration);

    const datasets = []
    for (let i = 0; i < valArray.length; i++) {
        datasets[i] = {
            // label: 'Speed 1',
            data: [valArray[i]],
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderWidth: 3,
            barPercentage: barPercentages[i] * 6, // Adjust barPercentage to control the width of the first bar
            categoryPercentage: 0.95,
            skipNull: false,
        }
    }

    return datasets

}

function createPlot2(data) {
    const ctxS = document.getElementById('ChartS2').getContext('2d');
    const ctxH = document.getElementById('ChartH2').getContext('2d');
    const speedarr = data.map(lap => parseFloat(lap.speed.avg));
    const heartarr = data.map(lap => parseFloat(lap.heartRate.max));
    const duration = data.map(lap => parseInt(lap.duration));

    datasets_speed = createDataset(speedarr, duration)
    datasets_hr = createDataset(heartarr, duration)

    const datainp_hr = {
        labels: ["All"],
        datasets: datasets_hr,
        categoryPercentage: 1,
    }

    const datainp_speed = {
        labels: ["All"],
        datasets: datasets_speed,
        categoryPercentage: 1,
    }
    const options = {
        scales: {
            y: {
                beginAtZero: false
            },
        },
        plugins: {
            legend: { display: false }
        },
    };

    const myChartS = new Chart(ctxS, {
        type: 'bar',
        data: datainp_speed,
        options: options
    });
    window.ChartS2 = myChartS;

    const myChartH = new Chart(ctxH, {
        type: 'bar',
        data: datainp_hr,
        options: options
    });
    window.ChartH2 = myChartH;
    toHeadofpage()
}

function plotje(data) {
    const ctxS = document.getElementById('ChartS1').getContext('2d');
    const ctxH = document.getElementById('ChartH1').getContext('2d');
    const heartarr = data.map(lap => parseFloat(lap.heartRate.max));
    const speedarr = data.map(lap => parseFloat(lap.speed.avg));
    const duration = data.map(lap => parseInt(lap.duration));

    if (!window.ChartS1 || !(window.ChartS1 instanceof Chart)) {
        datasets_speed = createDataset(speedarr, duration)
        const datainp_speed = {
            labels: ["All"],
            datasets: datasets_speed,
            categoryPercentage: 1,
        }

        datasets_hr = createDataset(heartarr, duration)
        const datainp_hr = {
            labels: ["All"],
            datasets: datasets_hr,
            categoryPercentage: 1,
        }


        const options = {
            scales: {
                y: {
                    beginAtZero: false
                },
            },
            plugins: {
                legend: { display: false }
            },
        };

        const myChartS = new Chart(ctxS, {
            type: 'bar',
            data: datainp_speed,
            options: options
        });
        window.ChartS1 = myChartS;

        const myChartH = new Chart(ctxH, {
            type: 'bar',
            data: datainp_hr,
            options: options
        });
        window.ChartH1 = myChartH;


        toHeadofpage()
    }

    else {
        if (window.ChartS2 && window.ChartS2 instanceof Chart) {
            window.ChartS2.destroy();
        }
        if (window.ChartH2 && window.ChartH2 instanceof Chart) {
            window.ChartH2.destroy();
        }
        createPlot2(data)
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

