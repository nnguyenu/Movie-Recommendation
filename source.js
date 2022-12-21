console.log('Hello World again');
const N = 7;
let k = 0;
for (k = 0; k < N; k++) {
    if(k % 2 === 0) { 
        console.log( k );
    }
}
// string is immutable (cannot changed a single character)
let myStr = "This is a \"double quote\" string";
myStrLength = myStr.length;
console.log(myStr, myStrLength);

function myFunction(noun, adjective, verb, adverb) {
    let res = ""
    res += "The " + adjective + " " + noun + " " + verb + " to my home " + adverb + ".";
    return res;
}
console.log(myFunction("dog", "big", "ran", "quickly"));

let arr = [1,"str",3.14,true,[0,3]];
arr.push([10,100]); // like append python
let last_elem = arr.pop(); // like pop python
let first_elem = arr.shift(); // like pop(0) python
arr.unshift("1st"); // like insert(0) python
console.log(arr, last_elem, first_elem);
console.log(typeof arr, typeof myStr, typeof first_elem, typeof undefined_variable);

// document: a global build-in variable. Represent the loaded webpage
// querySelector: select the 1st element matching the parameter follows CSS selector syntax
let element = document.querySelector('h1');
console.log(element);
element.textContent = "Modified in JavaScript !"; // modify the text content of the element

const p_element = document.querySelector('p');
for(let k = 0; k < 5; k++) {
    p_element.textContent += "Hello world "+k+" ";
}

// create a new <h2> element
const newElement = document.createElement("h2"); 
newElement.textContent = "Some created title";
const parentElement = document.querySelector("body"); 
parentElement.appendChild(newElement);

for(let k = 0; k < 4; k++) {
    const paragraphElement = document.createElement("p");
    paragraphElement.textContent = "Paragraph "+k; 
    document.querySelector("body").appendChild(paragraphElement);
}

// changing style
let titleElement = document.querySelector('h1'); 
titleElement.style = "background-color:lightblue";
let strongElement = document.querySelector('strong');
strongElement.style = "color:red";

let click_counter = 0;
function actionClick(event) { 
    console.log('Mouse clicked !');
    click_counter += 1;
    strongElement.textContent = "Click counter: "+click_counter;

    const button = event.button; 
    const x = event.clientX; 
    const y = event.clientY;
    const newElement = document.createElement('p'); 
    newElement.textContent = `Click ${button} at position (${x},${y})`;
    document.querySelector("body").appendChild(newElement);
}
document.addEventListener('click', actionClick);

const h1Element = document.querySelector("h1");
h1Element.addEventListener('click', actionTitleClick); 
function actionTitleClick(event) { 
    h1Element.textContent = "Title clicked !";
}

document.querySelector(".ballon1").addEventListener('click', actionExplode);

function actionExplode(event) {
    const ballon = event.target;
    ballon.style = "display:none";
}