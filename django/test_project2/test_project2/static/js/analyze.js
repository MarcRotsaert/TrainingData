function plotLapdata(cell) {
    const fname = cell.getAttribute("value");
    const url = cell.getAttribute("data-url");
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


function _createDataset(valArray, duration, backgroundColor) {
    const totalDuration = duration.reduce((total, duration) => total + duration, 0);
    const barPercentages = duration.map(duration => duration / totalDuration);

    const durationMin = duration.map(d => (d / 60).toFixed(1));

    let datasets = []
    for (let i = 0; i < valArray.length; i++) {
        datasets[i] = {
            label: 'L ' + (i + 1) + "\nduration:" + durationMin[i] + 'min\n',
            data: [valArray[i]],
            backgroundColor: backgroundColor,
            borderWidth: 2,
            barPercentage: barPercentages[i] * 6, // Adjust barPercentage to control the width of the first bar
            categoryPercentage: 0.95,
            skipNull: false,
        }
    }
    return datasets
}


function _createBarDatainp(datasets, duration) {
    const datainp = {
        labels: [""],
        // labels: [duration],
        datasets: datasets,
        categoryPercentage: 1,
        duration: duration,
    }
    return datainp
}


function _getYaxisLimit(chartid, arr) {
    arr_min = Math.min(...arr)
    arr_max = Math.max(...arr)
    handle = chartid + "1"
    if (window[handle] && window[handle] instanceof Chart) {
        window[handle].scales.y.min < arr_min ? ymin = window[handle].scales.y.min : ymin = arr_min
        window[handle].scales.y.max > arr_max ? ymax = window[handle].scales.y.max : ymax = arr_max
        return [ymin, ymax]
    }

}

function _createOptions(customOptions = {}) {
    const defaultOptions = {
        clip: true,
        aspectRatio: 2.5,
        scales: {
            y: {
                beginAtZero: false,
                // max: 200,
            },
            alignToPixels: false,
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

    const options = { ...defaultOptions, ...customOptions };

    return options
}


function _data2array(data) {
    const lapdata = data["lapdata"]
    const ldate = data["ldate"]
    const heartarr = lapdata.map(lap => parseFloat(lap.heartRate.avg));
    const speedarr = lapdata.map(lap => parseFloat(lap.speed.avg_corr ? lap.speed.avg_corr : lap.speed.avg));
    const duration = lapdata.map(lap => parseInt(lap.duration));
    return { speedarr, heartarr, duration, ldate };
}


function plotje(data) {
    // const ctxS = document.getElementById('ChartS1').getContext('2d');
    // const ctxH = document.getElementById('ChartH1').getContext('2d');

    // const { speedarr, heartarr, heartmaxarr, duration, ldate } = _data2array(data);
    // const { speedarr, heartarr, duration, ldate } = _data2array(data);
    // console.log(ldate)

    if (!window.ChartS1 || !(window.ChartS1 instanceof Chart)) {
        // console.log(window.ChartS1.options)
        createPlotsTraining(data, 1)
    }
    else {
        _destroygraph("ChartS2")
        _destroygraph("ChartH2")
        createPlotsTraining(data, 2)
    }
}

function _destroygraph(graphid) {
    if (window[graphid] && window[graphid] instanceof Chart) {
        window[graphid].destroy()
        window[graphid] = undefined
    }
}

function resetgraphs() {
    const graphids = ["ChartS1", "ChartS2", "ChartH1", "ChartH2"]
    for (let i of graphids) {
        _destroygraph(i)
    }

    elem = document.getElementById("ldate1")
    elem.textContent = ""
    elem = document.getElementById("ldate2")
    elem.textContent = ""
}

function _returnPlotVariables(parameter, data) {
    const { speedarr, heartarr, duration, ldate } = _data2array(data);
    let arr, chart_id, tick;
    if (parameter == "heartRate") {
        arr = heartarr
        chart_id = "ChartH"
        tick = { stepSize: 10 }
    }

    else if (parameter == "speed") {
        arr = speedarr
        chart_id = "ChartS"
        tick = { stepSize: 1 }
    }
    return { arr, duration, chart_id, tick };
}


function _createPlot(data, parameter, nr) {
    let { arr, duration, chart_id, tick } = _returnPlotVariables(parameter, data)
    chart_h = chart_id + nr
    extraoptions = {}
    // extraoptions = { plugins: {}, legend: { display: false } }

    yaxlim = _getYaxisLimit(chart_id, arr)
    if (yaxlim) {
        extraoptions.scales = {
            y: {
                beginAtZero: false, min: yaxlim[0], max: yaxlim[1],
                ticks: tick,
            }
        }
        window[chart_id + "1"].config.options.scales.y.min = yaxlim[0]
        window[chart_id + "1"].config.options.scales.y.max = yaxlim[1]
        window[chart_id + "1"].update()
    }
    else {
        extraoptions.scales = {
            y: {
                beginAtZero: false,
                ticks: tick
            }
        }
    }

    if (parameter == "speed") {
        backgroundColor = 'rgba(200, 0, 0, 0.2)'
    }
    else if (parameter == "heartRate") {
        backgroundColor = 'rgba(0, 200, 0, 0.2)'
    }


    options = _createOptions(extraoptions)
    dataset = _createDataset(arr, duration, backgroundColor)
    datainp = _createBarDatainp(dataset)
    const ctx = document.getElementById(chart_h).getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: datainp,
        options: options
    });
    let propertyNameS = chart_h;
    // window.ChartS2 = myChartS;
    window[propertyNameS] = myChart;

}


function createPlotsTraining(data, nr) {
    const { dummy1, dummy2, duration, ldate } = _data2array(data);
    _createPlot(data, "speed", nr)
    _createPlot(data, "heartRate", nr)

    elem = document.getElementById("ldate" + nr)
    elem.innerHTML = ldate;
    toHeadofpage()

}


