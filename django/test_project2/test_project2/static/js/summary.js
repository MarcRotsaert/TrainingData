function showLapdata(cell) {
    const fname = cell.parentNode.getAttribute("value")
    const url = cell.parentNode.getAttribute("data-url")
    console.log(url)
    console.log(fname)

    // Use AJAX to send the data to the Django view
    make_xhr("GET", fname, url)
    toHeadofpage()
}