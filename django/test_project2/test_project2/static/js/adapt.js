function showAdapt(cell) {
    const fname = cell.getAttribute("value")
    const url = cell.getAttribute("data-url")
    const elem1 = document.getElementById("rb_delete")
    const elem2 = document.getElementById("rb_update")
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


function showAdaptLap(cell) {
    const fname = cell.parentNode.parentNode.getAttribute("value")
    const url = cell.parentNode.parentNode.getAttribute("data-url")
    const lapnr = cell.cells[0].textContent
    console.log(lapnr)
    make_xhr("POST", fname, url, { "lapnr": lapnr })
    toHeadofpage()
}
