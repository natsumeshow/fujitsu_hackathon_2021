//calendar
var events = [
    {'Date': new Date(2021, 1, 7), 'Title': '運動量: 100000'},
    {'Date': new Date(2021, 2, 18), 'Title': '運動量: 999999'},
    {'Date': new Date(2021, 1, 27), 'Title': '運動量: 120'},
];
  
var settings = {};
var element = document.getElementById('caleandar');
caleandar(element, events, settings);

function backToMenu(){
    location.href = "select.html";
}

/*
function loadEvents(){
    eel.loadEvents_p();
}
*/