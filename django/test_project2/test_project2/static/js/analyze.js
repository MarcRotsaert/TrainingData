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

// function _createDatasetPoint(valArray, duration) {
//     const pointDatasets = [];
//     for (let i = 0; i < valArray.length; i++) {
//         const points = [];
//         const durationSum = duration.slice(0, i + 1).reduce((total, duration) => total + duration, 0);
//         for (let j = 0; j < durationSum; j++) {
//             points.push(valArray[i]);
//         }
//         pointDatasets.push({
//             label: 'L ' + (i + 1) + ' points',
//             data: points,
//             backgroundColor: 'rgba(255, 99, 132, 0.2)',
//             borderWidth: 3,
//             barPercentage: barPercentages[i] * 6,
//             categoryPercentage: 0.95,
//             skipNull: false,
//         });
//     }
//     return pointDatasets;


// }

function _createDataset(valArray, duration) {
    const totalDuration = duration.reduce((total, duration) => total + duration, 0);
    const barPercentages = duration.map(duration => duration / totalDuration);

    let durationMin = duration.map(d => (d / 60).toFixed(1));

    const datasets = []
    for (let i = 0; i < valArray.length; i++) {
        datasets[i] = {
            label: 'L ' + (i + 1) + "\nduration:" + durationMin[i] + 'min\n',
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


function _bardatainp(datasets, duration) {
    const datainp = {
        labels: [""],
        // labels: [duration],
        datasets: datasets,
        categoryPercentage: 1,
        duration: duration,
    }
    return datainp
}


function _creatOptions() {
    const options = {
        scales: {
            y: {
                beginAtZero: false,
                // max: 200,
            },
        },
        plugins: {
            legend: { display: false },
            tooltip: {
                backgroundColor: 'rgba(200, 0, 0, 0.5)',
                // callbacks: {
                //     label: function (tooltipItems, data) {
                //         console.log(data)
                //         // const text = chartData[tooltipItems.datasetIndex]
                //         return tooltipItems.datasetIndex;
                //     },

                // }
            },

        }
    };

    return options
}


function _data2array(data) {
    var lapdata = data["lapdata"]
    const ldate = data["ldate"]
    const heartarr = lapdata.map(lap => parseFloat(lap.heartRate.avg));
    // const heartmaxarr = lapdata.map(lap => parseFloat(lap.heartRate.avg));
    // const speedarrcorr = lapdata.map(lap => parseFloat(lap.speed.avg_corr));
    const speedarr = lapdata.map(lap => parseFloat(lap.speed.avg_corr ? lap.speed.avg_corr : lap.speed.avg));
    const duration = lapdata.map(lap => parseInt(lap.duration));
    // return { speedarr, heartarr, heartmaxarr, duration, ldate };
    return { speedarr, heartarr, duration, ldate };
}


function plotje(data) {
    const ctxS = document.getElementById('ChartS1').getContext('2d');
    const ctxH = document.getElementById('ChartH1').getContext('2d');

    // const { speedarr, heartarr, heartmaxarr, duration, ldate } = _data2array(data);
    const { speedarr, heartarr, duration, ldate } = _data2array(data);
    console.log(ldate)



    if (!window.ChartS1 || !(window.ChartS1 instanceof Chart)) {
        console.log(window.ChartS1.options)
        createPlot(data, 1)

    }

    else {
        _destroygraph("ChartS2")
        _destroygraph("ChartH2")
        createPlot(data, 2)
    }
}

function _destroygraph(graphid) {
    if (window[graphid] && window[graphid] instanceof Chart) {
        window[graphid].destroy()
        window[graphid] = undefined
    }
}

function resetgraphs() {
    graphids = ["ChartS1", "ChartS2", "ChartH1", "ChartH2"]
    for (let i of graphids) {
        _destroygraph(i)
    }

    elem = document.getElementById("ldate1")
    elem.textContent = ""
    elem = document.getElementById("ldate2")
    elem.textContent = ""
}

function createPlot(data, nr) {
    const ctxS = document.getElementById('ChartS' + nr).getContext('2d');
    const ctxH = document.getElementById('ChartH' + nr).getContext('2d');

    // const { speedarr, heartarr, heartmaxarr, duration, ldate } = _data2array(data);
    const { speedarr, heartarr, duration, ldate } = _data2array(data);

    datasets_speed = _createDataset(speedarr, duration)
    datasets_hr = _createDataset(heartarr, duration)

    datainp_speed = _bardatainp(datasets_speed)
    datainp_hr = _bardatainp(datasets_hr)

    options = _creatOptions()

    const myChartS = new Chart(ctxS, {
        type: 'bar',
        data: datainp_speed,
        options: options
    });

    let propertyNameS = 'ChartS' + nr;
    // window.ChartS2 = myChartS;
    window[propertyNameS] = myChartS;

    const myChartH = new Chart(ctxH, {
        type: 'bar',
        data: datainp_hr,
        options: options
    });
    let propertyNameH = 'ChartH' + nr;
    // window.ChartS2 = myChartS;
    window[propertyNameH] = myChartH;
    // window.ChartH2 = myChartH;

    elem = document.getElementById("ldate" + nr)
    elem.innerHTML = ldate;
    toHeadofpage()
}


function toHeadofpage() {
    window.scrollTo(0, 0);
}
