function myFunction() {
    return Date();
    // return 'yes sir';
}

function myFunction2() {
    return console.log(myFunction())
}

function changeButtonTitle() {
    var button = document.getElementById("myButton");
    button.textContent = "Supply!!"
    console.log(button.textContent)
}
