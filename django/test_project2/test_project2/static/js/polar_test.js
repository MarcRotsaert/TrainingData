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
            label: 'Speed 1',
            data: [valArray[i]],
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderWidth: 1,
            barPercentage: barPercentages[i] * 3, // Adjust barPercentage to control the width of the first bar
        }

    }

    return datasets

}


function plotje(data) {
    const ctx = document.getElementById('myChart').getContext('2d');

    const speedarr = data.map(lap => parseFloat(lap.speed.avg));
    const duration = data.map(lap => parseInt(lap.duration));

    if (window.myChart && window.myChart instanceof Chart) {
        window.myChart.destroy();
    }
    // console.log(window.myChart)
    // console.log(window.myChart instanceof Chart)
    datasets = createDataset(speedarr, duration)
    const datainp = {
        labels: ["All"],
        datasets: datasets,
        categoryPercentage: 1,
    }

    const options = {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    };

    const myChart = new Chart(ctx, {
        type: 'bar',
        data: datainp,
        options: options
    });
    window.myChart = myChart;
    toHeadofpage()
}

function plotje2(data) {
    console.log(data);
    const ctx = document.getElementById('myChart');
    const lapnr = data.map(lap => parseInt(lap.lapNumber) + 1);
    const speedarr = data.map(lap => parseFloat(lap.speed.avg));
    const duration = data.map(lap => parseInt(lap.duration));

    if (window.myChart instanceof Chart) {
        window.myChart.destroy();
    }

    const totalDuration = duration.reduce((total, duration) => total + duration, 0);
    const barPercentages = duration.map(duration => duration / totalDuration);
    console.log(barPercentages)
    const datasets = [{
        label: 'Speed',
        data: [10, 30],
        // barPercentage: barPercentages.map(percentage => percentage * 0.9),
        barPercentage: [1, 1],
        // categoryPercentage: 0.8,
        backgroundColor: ['rgba(255, 99, 132, 0.2)', 'rgba(255, 99, 132, 0.2)'],
        borderWidth: 10

    }];

    window.myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            // labels: ['All Laps'], // Single category for all laps
            datasets: datasets
        },
        // options: {
        //     scales: {
        //         y: {
        //             beginAtZero: true,
        //             title: {
        //                 display: true,
        //                 text: 'Speed'
        //             }
        //         },
        //         x: {
        //             title: {
        //                 display: true,
        //                 text: 'Lap Number'
        //             }
        //         }
        //     }
        // }
    });
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

