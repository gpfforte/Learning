let a = 3;
console.log("a =", a)
a = document.getElementById("body_title").innerHTML

document.getElementById("body_title").innerHTML = a + " as a Ninja"
console.log("a =", a)

console.log(document.lastModified)
console.log(formatDate(document.lastModified));