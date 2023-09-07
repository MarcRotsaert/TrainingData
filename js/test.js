import Math

const conti = 1
let leti
var vari
vari = (1 === '1' || 2 == 2)

vari.valueOf()

if (false) {
    if (1 === '1' || 1 !== true) {
        console.log('yes')
    }
    else if (2 == 3) {
        console.log('yesyes')
    }
    else {
        console.log('bleee')
    }
}

if (false) {
    let isgood = (1 === '1' || 1 !== true)
    var result = isgood ? true : false
    console.log(result)
    for (i = 1; i < 10; i++) { console.log(i) }
    var i = 'value'
    for (let i = 1; i < 10; i++) { console.log(i) }
    console.log(i)
    console.log(i.length)
    console.log(i.padEnd(10, '_'))
}

if (false) {
    function getvalue(i) { return i }

    var value = 10
    i = getvalue(value)
    console.log(i)



    var robj = {
        getValue: getvalue,
        otherValue: 10,
        getRandomValue: Math.random()
    }

    console.log(Math.random())

    console.log(robj.otherValue)
    console.log(robj.getValue(5))
    console.log(robj.getRandomValue)
}
if (false) {
    let x = 10;
    x ||= 5; console.log(x)
    dosomething1 = function (y) { return (y + 1) }
    dosomething2 = function addone(y) { return (y + 1) }

    console.log(dosomething1(10))
    console.log(dosomething2(10))

    harry = [1, '2', null, undefined]
    // console.log(harry.length)
    // console.log(harry[0])
    y = harry.forEach(dosomething1)
    console.log(y)

    x = harry.map(dosomething1)
    console.log(x)

    console.log(harry.pop())
}

// STRING
var x = "stringie"
y = x.slice(1, 3)
// var x = Array("ja", "nee")
// console.log(x.filter())
// console.log(x[0])

let text = "Please locate where 'locate' occurs!";
text.search("locate");
text.search(/locate/)