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
