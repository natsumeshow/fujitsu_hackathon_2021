//calendar

/*
var events = [
    {'Date': new Date(2021, 1, 7), 'Title': '運動量: 100000'},
    {'Date': new Date(2021, 2, 18), 'Title': '運動量: 999999'},
    {'Date': new Date(2021, 1, 27), 'Title': '運動量: 120'},
];
*/
  
var events_arr = [];
loadEvents();
setTimeout(function(){
    console.log(events_arr);
    var events = [];
    var settings = {};
    for(var i=0;i<events_arr.length;i+=4){
        var tmp = {"Date": new Date(events_arr[i], events_arr[i+1], events_arr[i+2]), "Title": "運動量:"+events_arr[i+3]+"pt"};
        events.push(tmp);   
    }
    var element = document.getElementById('caleandar');
    caleandar(element, events, settings);
},1000);

async function loadEvents() {
    events_arr = await eel.read_movement()();
    console.log(events_arr);
}

function backToMenu(){
    location.href = "select.html";
}